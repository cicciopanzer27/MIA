import json
import time
import uuid
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class AgentState:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    clock: int = 0
    knowledge: Dict[str, Any] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    energy: float = 100.0
    status: str = "active"

class SymbolicBridge:
    """Bridge per comunicare con il Kernel Simbolico Nativo in Clojure"""
    
    def __init__(self):
        self.clojure_path = "clj"
        
    def execute_clojure(self, code: str) -> Dict:
        """Esegue codice Clojure e ritorna il risultato"""
        try:
            cmd = [self.clojure_path, "-M", "-e", code]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {"success": True, "result": result.stdout.strip()}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_atom(self, element: str) -> Dict:
        """Crea un atomo simbolico"""
        code = f"""
        (require '[mia.core :as core])
        (println (pr-str (core/create-atom :{element})))
        """
        return self.execute_clojure(code)
    
    def compose_molecule(self, atoms: List[Dict]) -> Dict:
        """Compone atomi in una molecola"""
        atoms_str = str(atoms).replace("'", "")
        code = f"""
        (require '[mia.algebras :as alg])
        (println (pr-str (alg/compose-atoms {atoms_str})))
        """
        return self.execute_clojure(code)
    
    def infer_properties(self, entity: Dict) -> Dict:
        """Inferisce proprietà di un'entità"""
        entity_str = str(entity).replace("'", "")
        code = f"""
        (require '[mia.inference :as inf])
        (println (pr-str (inf/infer-properties {entity_str} {{}})))
        """
        return self.execute_clojure(code)

class BaseAgent(ABC):
    """Classe base per tutti gli agenti del sistema MIA"""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.state = AgentState(id=agent_id or str(uuid.uuid4()))
        self.bridge = SymbolicBridge()
        self.last_tick = time.time()
        
    def tick(self) -> None:
        """Incrementa il clock interno dell'agente"""
        self.state.clock += 1
        self.last_tick = time.time()
        
        # Decrementa energia per simulare consumo
        self.state.energy = max(0, self.state.energy - 0.1)
        
        if self.state.energy <= 0:
            self.state.status = "exhausted"
    
    @abstractmethod
    def act(self) -> Dict[str, Any]:
        """Fase ACT: L'agente decide un'azione basata sul suo stato"""
        pass
    
    def share(self, message: Dict[str, Any]) -> None:
        """Fase SHARE: Pubblica un messaggio sul backplane"""
        message.update({
            "sender_id": self.state.id,
            "timestamp": time.time(),
            "clock": self.state.clock
        })
        # TODO: Implementare pubblicazione su Redis
        print(f"Agent {self.state.id[:8]} shares: {message}")
    
    def sync(self) -> List[Dict[str, Any]]:
        """Fase SYNC: Legge messaggi dal backplane"""
        # TODO: Implementare lettura da Redis
        # Per ora simula con lista vuota
        return []
    
    def run_cycle(self) -> None:
        """Esegue un ciclo completo Tick-Act-Share-Sync"""
        if self.state.status != "active":
            return
            
        # TICK
        self.tick()
        
        # ACT
        action = self.act()
        
        # SHARE
        if action:
            self.share(action)
        
        # SYNC
        messages = self.sync()
        self.process_messages(messages)
    
    def process_messages(self, messages: List[Dict[str, Any]]) -> None:
        """Elabora i messaggi ricevuti dal backplane"""
        for msg in messages:
            if msg.get("sender_id") != self.state.id:  # Ignora i propri messaggi
                self.handle_message(msg)
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """Gestisce un singolo messaggio ricevuto"""
        # Implementazione base: aggiorna la conoscenza
        if "knowledge" in message:
            self.state.knowledge.update(message["knowledge"])

class ChemistAgent(BaseAgent):
    """Agente specializzato in chimica simbolica"""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id)
        self.state.goals = ["create_molecules", "discover_reactions"]
        self.known_atoms = {}
        self.known_molecules = {}
    
    def act(self) -> Dict[str, Any]:
        """Agente chimico: crea atomi, li combina in molecole"""
        if self.state.clock % 5 == 0:  # Ogni 5 tick, crea un nuovo atomo
            return self.create_random_atom()
        elif self.state.clock % 10 == 0:  # Ogni 10 tick, prova a fare una molecola
            return self.attempt_molecule_creation()
        else:
            return self.analyze_existing_knowledge()
    
    def create_random_atom(self) -> Dict[str, Any]:
        """Crea un atomo casuale"""
        import random
        elements = ["hydrogen", "carbon", "oxygen", "nitrogen"]
        element = random.choice(elements)
        
        result = self.bridge.create_atom(element)
        if result["success"]:
            atom_data = eval(result["result"])  # Parse Clojure output
            self.known_atoms[atom_data["id"]] = atom_data
            
            return {
                "type": "atom_created",
                "atom": atom_data,
                "knowledge": {f"atom_{atom_data['id']}": atom_data}
            }
        return {"type": "error", "message": result.get("error", "Unknown error")}
    
    def attempt_molecule_creation(self) -> Dict[str, Any]:
        """Prova a creare una molecola dagli atomi disponibili"""
        if len(self.known_atoms) < 2:
            return {"type": "insufficient_atoms", "count": len(self.known_atoms)}
        
        # Prende i primi due atomi disponibili
        atoms = list(self.known_atoms.values())[:2]
        result = self.bridge.compose_molecule(atoms)
        
        if result["success"] and "nil" not in result["result"]:
            molecule_data = eval(result["result"])
            self.known_molecules[molecule_data["id"]] = molecule_data
            
            return {
                "type": "molecule_created",
                "molecule": molecule_data,
                "knowledge": {f"molecule_{molecule_data['id']}": molecule_data}
            }
        
        return {"type": "molecule_creation_failed", "atoms": [a["id"] for a in atoms]}
    
    def analyze_existing_knowledge(self) -> Dict[str, Any]:
        """Analizza la conoscenza esistente per dedurre nuove proprietà"""
        if not self.known_molecules:
            return {"type": "no_analysis", "reason": "no_molecules"}
        
        molecule = list(self.known_molecules.values())[0]
        result = self.bridge.infer_properties(molecule)
        
        if result["success"]:
            enhanced_molecule = eval(result["result"])
            self.known_molecules[molecule["id"]] = enhanced_molecule
            
            return {
                "type": "properties_inferred",
                "molecule_id": molecule["id"],
                "new_properties": enhanced_molecule.get("properties", {}),
                "knowledge": {f"enhanced_{molecule['id']}": enhanced_molecule}
            }
        
        return {"type": "analysis_failed", "error": result.get("error")}

class PhysicsAgent(BaseAgent):
    """Agente specializzato in fisica simbolica"""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id)
        self.state.goals = ["model_fields", "compute_interactions"]
        self.field_models = {}
    
    def act(self) -> Dict[str, Any]:
        """Agente fisico: modella campi e interazioni"""
        # Cerca entità su cui applicare modelli fisici
        entities = list(self.state.knowledge.values())
        physical_entities = [e for e in entities if isinstance(e, dict) and "element" in e]
        
        if len(physical_entities) >= 2:
            return self.model_interaction(physical_entities[:2])
        elif physical_entities:
            return self.analyze_single_entity(physical_entities[0])
        else:
            return {"type": "waiting_for_entities", "knowledge_size": len(self.state.knowledge)}
    
    def model_interaction(self, entities: List[Dict]) -> Dict[str, Any]:
        """Modella l'interazione tra due entità"""
        entity1, entity2 = entities[:2]
        
        # Simula calcolo di campo elettromagnetico
        interaction = {
            "type": "electromagnetic_interaction",
            "entity1": entity1.get("id", "unknown"),
            "entity2": entity2.get("id", "unknown"),
            "force": self.calculate_symbolic_force(entity1, entity2),
            "field_strength": "symbolic_coulomb"
        }
        
        return {
            "type": "interaction_modeled",
            "interaction": interaction,
            "knowledge": {f"interaction_{entity1.get('id')}_{entity2.get('id')}": interaction}
        }
    
    def calculate_symbolic_force(self, e1: Dict, e2: Dict) -> str:
        """Calcola simbolicamente la forza tra due entità"""
        # Logica simbolica semplificata
        if e1.get("element") == "hydrogen" and e2.get("element") == "oxygen":
            return "attractive_covalent"
        elif e1.get("element") == e2.get("element"):
            return "repulsive_same_charge"
        else:
            return "weak_van_der_waals"
    
    def analyze_single_entity(self, entity: Dict) -> Dict[str, Any]:
        """Analizza una singola entità fisicamente"""
        analysis = {
            "entity_id": entity.get("id", "unknown"),
            "mass": f"symbolic_{entity.get('element', 'unknown')}_mass",
            "charge": entity.get("protons", 0) - entity.get("electrons", 0),
            "magnetic_moment": "spin_dependent",
            "quantum_state": "ground_state"
        }
        
        return {
            "type": "entity_analyzed",
            "analysis": analysis,
            "knowledge": {f"physics_{entity.get('id')}": analysis}
        }