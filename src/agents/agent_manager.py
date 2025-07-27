import time
import threading
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from .base_agent import BaseAgent, ChemistAgent, PhysicsAgent

class AgentManager:
    """Gestisce una società di agenti MIA"""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.running = False
        self.stats = {
            "total_cycles": 0,
            "active_agents": 0,
            "messages_shared": 0
        }
    
    def add_agent(self, agent: BaseAgent) -> None:
        """Aggiunge un agente alla società"""
        self.agents.append(agent)
        print(f"Added agent {agent.state.id[:8]} ({type(agent).__name__})")
    
    def create_default_society(self) -> None:
        """Crea una società di default con diversi tipi di agenti"""
        # 3 agenti chimici
        for i in range(3):
            self.add_agent(ChemistAgent(f"chemist_{i}"))
        
        # 2 agenti fisici
        for i in range(2):
            self.add_agent(PhysicsAgent(f"physics_{i}"))
        
        print(f"Created society with {len(self.agents)} agents")
    
    def run_single_cycle(self) -> None:
        """Esegue un singolo ciclo per tutti gli agenti"""
        active_count = 0
        
        # Esegue tutti gli agenti in parallelo
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = []
            for agent in self.agents:
                if agent.state.status == "active":
                    future = executor.submit(agent.run_cycle)
                    futures.append(future)
                    active_count += 1
            
            # Aspetta che tutti completino
            for future in futures:
                future.result()
        
        self.stats["total_cycles"] += 1
        self.stats["active_agents"] = active_count
    
    def run_continuous(self, max_cycles: int = 100, cycle_delay: float = 1.0) -> None:
        """Esegue il sistema in modo continuo"""
        self.running = True
        print(f"Starting continuous run for {max_cycles} cycles...")
        
        try:
            for cycle in range(max_cycles):
                if not self.running:
                    break
                
                print(f"\n=== CYCLE {cycle + 1} ===")
                self.run_single_cycle()
                self.print_stats()
                
                time.sleep(cycle_delay)
                
        except KeyboardInterrupt:
            print("\nStopping on user request...")
        finally:
            self.running = False
            print("\nSystem stopped.")
    
    def stop(self) -> None:
        """Ferma il sistema"""
        self.running = False
    
    def print_stats(self) -> None:
        """Stampa statistiche del sistema"""
        print(f"Stats: Cycles={self.stats['total_cycles']}, "
              f"Active={self.stats['active_agents']}, "
              f"Total_Agents={len(self.agents)}")
        
        # Stampa stato di alcuni agenti
        for agent in self.agents[:2]:  # Solo i primi 2 per brevità
            print(f"  {agent.state.id[:8]}: Energy={agent.state.energy:.1f}, "
                  f"Clock={agent.state.clock}, Knowledge={len(agent.state.knowledge)}")
    
    def get_system_knowledge(self) -> Dict[str, Any]:
        """Raccoglie tutta la conoscenza del sistema"""
        system_knowledge = {}
        for agent in self.agents:
            agent_knowledge = {
                "agent_id": agent.state.id,
                "agent_type": type(agent).__name__,
                "knowledge": agent.state.knowledge,
                "stats": {
                    "clock": agent.state.clock,
                    "energy": agent.state.energy,
                    "status": agent.state.status
                }
            }
            system_knowledge[agent.state.id] = agent_knowledge
        
        return system_knowledge

# Script di test
if __name__ == "__main__":
    manager = AgentManager()
    manager.create_default_society()
    manager.run_continuous(max_cycles=20, cycle_delay=2.0)