import json
import time
import uuid
import subprocess
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import random

# --- KSN BRIDGE ---
class KSNBridge:
    def __init__(self, lein_path="lein"):
        self.lein_path = lein_path

    def _execute(self, clojure_code: str) -> Dict:
        try:
            # Usiamo 'lein exec' che è più adatto per script singoli
            cmd = [self.lein_path, "exec", "-e", clojure_code]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return {"success": True, "result": json.loads(result.stdout.strip())}
            else:
                return {"success": False, "error": f"Clojure Error: {result.stderr}"}
        except json.JSONDecodeError:
            return {"success": False, "error": f"JSON Decode Error on output: {result.stdout}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_task(self, task: Dict) -> Dict:
        task_str = json.dumps(task).replace('"', '\\"')
        clojure_code = f"""
        (require 'mia.ksn)
        (require '[clojure.data.json :as json])
        (let [task-map (json/read-str \\"{task_str}\\" :key-fn keyword)
              result (mia.ksn/execute-task task-map)]
          (println (json/write-str result)))
        """
        return self._execute(clojure_code)

# --- AGENT DEFINITIONS ---
@dataclass
class AgentState:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    clock: int = 0
    knowledge_base: Dict[str, Any] = field(default_factory=dict)

class BaseAgent:
    def __init__(self, agent_id: str, bridge: KSNBridge, message_bus: list):
        self.state = AgentState(id=agent_id)
        self.bridge = bridge
        self.message_bus = message_bus

    def tick(self):
        self.state.clock += 1

    def act(self):
        # L'agente base non fa nulla, è solo un osservatore
        return None

    def share(self, message: Dict):
        full_message = {
            "sender_id": self.state.id,
            "timestamp": time.time(),
            "content": message
        }
        self.message_bus.append(full_message)
        print(f"[{self.state.id}] 📢 Shares: {message.get('type')} with data {message.get('atom', {}).get('id')}")

    def sync(self):
        messages_for_me = [
            msg for msg in self.message_bus if msg["sender_id"] != self.state.id
        ]
        for msg in messages_for_me:
            self.handle_message(msg['content'])

    def handle_message(self, content: Dict):
        if content.get("type") == "new_atom" and content.get("atom"):
            atom = content["atom"]
            if atom and atom.get('id'):
                self.state.knowledge_base[atom['id']] = atom
                print(f"[{self.state.id}] 🧠 Learned about atom: {atom['id']}")

    def run_cycle(self):
        print(f"[{self.state.id}] Starting cycle {self.state.clock + 1}")
        self.tick()
        self.sync()
        action_result = self.act()
        if action_result:
            self.share(action_result)

class ChemistAgent(BaseAgent):
    def act(self):
        if self.state.clock % 3 == 0:
            element = random.choice([":H", ":C", ":O"])
            task = {"task": ":create-atom", "payload": {"element": element}}
            print(f"[{self.state.id}] 🧪 Attempting to create atom {element}...")
            response = self.bridge.run_task(task)
            if response.get("success") and response.get("result"):
                return {"type": "new_atom", "atom": response["result"]}
            else:
                print(f"[{self.state.id}] ❌ KSN Bridge Error: {response.get('error')}")
        return None

# --- AGENT MANAGER ---
class AgentManager:
    def __init__(self):
        self.bridge = KSNBridge()
        self.message_bus = []
        self.agents: List[BaseAgent] = [
            ChemistAgent("Chemist-01", self.bridge, self.message_bus),
            BaseAgent("Observer-01", self.bridge, self.message_bus)
        ]

    def run_simulation(self, cycles: int):
        print("--- Starting MIA Simulation ---")
        for i in range(cycles):
            print(f"--- Cycle {i+1}/{cycles} ---")

            # In a real system, bus would be handled differently
            # For this simulation, we pass the whole bus and agents sync

            threads = []
            for agent in self.agents:
                thread = threading.Thread(target=agent.run_cycle)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            time.sleep(1)
        print("\n--- Simulation Ended ---")
        self.print_summary()

    def print_summary(self):
        print("\n--- Final Knowledge State ---")
        for agent in self.agents:
            print(f"Agent: {agent.state.id}")
            print(f"  Knowledge items: {len(agent.state.knowledge_base)}")
            for k, v in agent.state.knowledge_base.items():
                print(f"    - {k}: {v.get('element')}")

if __name__ == "__main__":
    manager = AgentManager()
    manager.run_simulation(10)