import time
import threading
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from .base_agent import BaseAgent

# Implementazioni specifiche degli agenti
class ChemistAgent(BaseAgent):
    """Agente specializzato in chimica"""
    
    def __init__(self, agent_id):
        super().__init__(agent_id, "ChemistAgent")
        self.atoms_created = 0
    
    def process(self):
        """Logica principale del chimico"""
        # Crea un atomo ogni 5 secondi circa
        if time.time() % 5 < 1:
            self.create_atom()
    
    def create_atom(self):
        """Crea un nuovo atomo e lo condivide"""
        self.atoms_created += 1
        atom_data = {
            'element': ['H', 'O', 'C', 'N'][self.atoms_created % 4],
            'id': f'atom_{self.agent_id}_{self.atoms_created}',
            'properties': {
                'mass': [1, 16, 12, 14][self.atoms_created % 4],
                'electrons': [1, 8, 6, 7][self.atoms_created % 4]
            }
        }
        
        print(f"[{self.agent_id}] 🧪 Creato atomo: {atom_data['element']}")
        self.share('atom', atom_data)
    
    def on_knowledge_received(self, knowledge_type, data, sender):
        """Reagisce alla conoscenza ricevuta"""
        if knowledge_type == 'analysis':
            print(f"[{self.agent_id}] 🧪 Ricevuta analisi da {sender}: {data.get('conclusion', 'N/A')}")
        elif knowledge_type == 'atom' and sender != self.agent_id:
            print(f"[{self.agent_id}] 🧪 Altro chimico ha creato: {data.get('element', 'Unknown')}")
    
    def get_capabilities(self):
        return ["atom_creation", "molecular_analysis", "chemical_reactions"]


class PhysicsAgent(BaseAgent):
    """Agente specializzato in fisica"""
    
    def __init__(self, agent_id):
        super().__init__(agent_id, "PhysicsAgent")
        self.analyses_performed = 0
    
    def process(self):
        """Logica principale del fisico"""
        # Analizza gli atomi ricevuti
        if 'atom' in self.knowledge_base:
            atoms = self.knowledge_base['atom']
            for atom_info in atoms:
                if not atom_info.get('analyzed', False):
                    self.analyze_atom(atom_info)
                    atom_info['analyzed'] = True
    
    def analyze_atom(self, atom_info):
        """Analizza un atomo e condivide l'analisi"""
        atom_data = atom_info['data']
        self.analyses_performed += 1
        
        analysis = {
            'atom_id': atom_data['id'],
            'element': atom_data['element'],
            'analysis_id': f'analysis_{self.agent_id}_{self.analyses_performed}',
            'properties_calculated': {
                'binding_energy': atom_data['properties']['electrons'] * 13.6,  # eV approssimativo
                'stability': 'stable' if atom_data['properties']['electrons'] <= 8 else 'reactive'
            },
            'conclusion': f"Atomo {atom_data['element']} analizzato - {'Stabile' if atom_data['properties']['electrons'] <= 8 else 'Reattivo'}"
        }
        
        print(f"[{self.agent_id}] ⚛️  Analisi completata per {atom_data['element']}")
        self.share('analysis', analysis)
    
    def on_knowledge_received(self, knowledge_type, data, sender):
        """Reagisce alla conoscenza ricevuta"""
        if knowledge_type == 'atom':
            print(f"[{self.agent_id}] ⚛️  Nuovo atomo da analizzare: {data.get('element', 'Unknown')}")
        elif knowledge_type == 'analysis' and sender != self.agent_id:
            print(f"[{self.agent_id}] ⚛️  Altro fisico ha analizzato: {data.get('element', 'Unknown')}")
    
    def get_capabilities(self):
        return ["atomic_analysis", "quantum_calculations", "energy_predictions"]


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
        print(f"✅ Aggiunto agente {agent.agent_id} ({agent.agent_type})")
    
    def create_default_society(self) -> None:
        """Crea una società di default con diversi tipi di agenti"""
        # 2 agenti chimici
        for i in range(2):
            self.add_agent(ChemistAgent(f"ChemistAgent_{i:03d}"))
        
        # 2 agenti fisici
        for i in range(2):
            self.add_agent(PhysicsAgent(f"PhysicsAgent_{i:03d}"))
        
        print(f"🏗️  Società creata con {len(self.agents)} agenti")
    
    def run_single_cycle(self) -> None:
        """Esegue un singolo ciclo per tutti gli agenti"""
        active_count = 0
        
        # Esegue tutti gli agenti in parallelo
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = []
            for agent in self.agents:
                if agent.active:
                    future = executor.submit(agent.process)
                    futures.append(future)
                    active_count += 1
            
            # Aspetta che tutti completino
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Errore nell'agente: {e}")
        
        self.stats["total_cycles"] += 1
        self.stats["active_agents"] = active_count
    
    def run_continuous(self, max_cycles: int = 20, cycle_delay: float = 3.0) -> None:
        """Esegue il sistema in modo continuo"""
        self.running = True
        print(f"🚀 Avvio sistema MIA per {max_cycles} cicli...\n")
        
        try:
            for cycle in range(max_cycles):
                if not self.running:
                    break
                
                print(f"\n{'='*50}")
                print(f"🔄 CICLO {cycle + 1}/{max_cycles}")
                print(f"{'='*50}")
                
                self.run_single_cycle()
                self.print_stats()
                
                time.sleep(cycle_delay)
                
        except KeyboardInterrupt:
            print("\n⏹️  Sistema fermato dall'utente...")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Ferma il sistema e tutti gli agenti"""
        self.running = False
        for agent in self.agents:
            agent.stop()
        print("🛑 Sistema MIA fermato.")
    
    def print_stats(self) -> None:
        """Stampa statistiche del sistema"""
        print(f"\n📊 Stats: Cicli={self.stats['total_cycles']}, "
              f"Agenti_Attivi={self.stats['active_agents']}")
        
        # Stampa stato degli agenti
        for agent in self.agents:
            kb_size = sum(len(knowledge) for knowledge in agent.knowledge_base.values())
            agent_type_short = agent.agent_type.replace('Agent', '')
            print(f"   🤖 {agent.agent_id}: KB={kb_size} elementi")
    
    def get_system_knowledge(self) -> Dict[str, Any]:
        """Raccoglie tutta la conoscenza del sistema"""
        system_knowledge = {}
        for agent in self.agents:
            agent_knowledge = {
                "agent_id": agent.agent_id,
                "agent_type": agent.agent_type,
                "knowledge_base": agent.knowledge_base,
                "capabilities": agent.get_capabilities()
            }
            system_knowledge[agent.agent_id] = agent_knowledge
        
        return system_knowledge
    
    def demonstrate_collective_intelligence(self):
        """Dimostra l'intelligenza collettiva del sistema"""
        print("\n🧠 DIMOSTRAZIONE INTELLIGENZA COLLETTIVA")
        print("="*60)
        
        # Statistiche finali
        total_knowledge = 0
        for agent in self.agents:
            agent_kb_size = sum(len(knowledge) for knowledge in agent.knowledge_base.values())
            total_knowledge += agent_kb_size
            print(f"🤖 {agent.agent_id}:")
            for knowledge_type, items in agent.knowledge_base.items():
                if items:
                    print(f"   - {knowledge_type}: {len(items)} elementi")
        
        print(f"\n🎯 RISULTATO: Il sistema ha generato {total_knowledge} elementi di conoscenza!")
        print("   📈 Gli agenti hanno collaborato creando, analizzando e condividendo informazioni")
        print("   🔄 La conoscenza è fluita automaticamente tra diversi tipi di agenti")


# Script di test principale
if __name__ == "__main__":
    print("🌟 MIA - Meta-Intelligence Agent Framework")
    print("=" * 50)
    
    manager = AgentManager()
    manager.create_default_society()
    
    print("\n⚠️  Per fermare il sistema: Ctrl+C")
    print("🔍 Osserva come gli agenti creano, condividono e analizzano conoscenza...\n")
    
    manager.run_continuous(max_cycles=15, cycle_delay=4.0)
    manager.demonstrate_collective_intelligence()