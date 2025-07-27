import redis
import json
import threading
import time
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, agent_id, agent_type):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.knowledge_base = {}
        self.active = True
        
        # Connessione Redis per comunicazione multi-agente
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            self.redis_client.ping()  # Test connessione
            print(f"[{self.agent_id}] Connesso a Redis backplane")
        except redis.ConnectionError:
            print(f"[{self.agent_id}] ERRORE: Impossibile connettersi a Redis")
            self.redis_client = None
        
        # Canali Redis
        self.broadcast_channel = "mia_broadcast"
        self.private_channel = f"mia_{self.agent_id}"
        
        # Thread per ascoltare messaggi
        self.listener_thread = threading.Thread(target=self._listen_messages, daemon=True)
        self.listener_thread.start()
    
    def share(self, knowledge_type, data, target_agent=None):
        """
        Condivide conoscenza via Redis
        
        Args:
            knowledge_type (str): Tipo di conoscenza (es: 'atom', 'analysis', 'hypothesis')
            data (dict): Dati da condividere
            target_agent (str, optional): ID agente specifico, None per broadcast
        """
        if not self.redis_client:
            print(f"[{self.agent_id}] Redis non disponibile, impossibile condividere")
            return False
        
        message = {
            'sender': self.agent_id,
            'sender_type': self.agent_type,
            'knowledge_type': knowledge_type,
            'data': data,
            'timestamp': time.time()
        }
        
        try:
            if target_agent:
                # Messaggio privato
                channel = f"mia_{target_agent}"
                self.redis_client.publish(channel, json.dumps(message))
                print(f"[{self.agent_id}] Inviato {knowledge_type} a {target_agent}")
            else:
                # Broadcast a tutti gli agenti
                self.redis_client.publish(self.broadcast_channel, json.dumps(message))
                print(f"[{self.agent_id}] Broadcast {knowledge_type} a tutti gli agenti")
            
            return True
        except Exception as e:
            print(f"[{self.agent_id}] Errore condivisione: {e}")
            return False
    
    def sync(self):
        """
        Sincronizza la knowledge base con i dati ricevuti
        Questa funzione è chiamata automaticamente dal listener
        """
        # La sincronizzazione avviene automaticamente tramite _listen_messages
        pass
    
    def _listen_messages(self):
        """
        Thread che ascolta i messaggi Redis in background
        """
        if not self.redis_client:
            return
        
        # Sottoscrivi ai canali
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(self.broadcast_channel, self.private_channel)
        
        print(f"[{self.agent_id}] In ascolto su canali: {self.broadcast_channel}, {self.private_channel}")
        
        for message in pubsub.listen():
            if not self.active:
                break
                
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    
                    # Non processare i propri messaggi
                    if data['sender'] == self.agent_id:
                        continue
                    
                    print(f"[{self.agent_id}] Ricevuto {data['knowledge_type']} da {data['sender']}")
                    
                    # Processa il messaggio
                    self._process_received_knowledge(data)
                    
                except json.JSONDecodeError:
                    print(f"[{self.agent_id}] Messaggio malformato ricevuto")
                except Exception as e:
                    print(f"[{self.agent_id}] Errore processing messaggio: {e}")
    
    def _process_received_knowledge(self, message_data):
        """
        Processa la conoscenza ricevuta da altri agenti
        
        Args:
            message_data (dict): Dati del messaggio ricevuto
        """
        knowledge_type = message_data['knowledge_type']
        data = message_data['data']
        sender = message_data['sender']
        
        # Aggiungi alla knowledge base
        if knowledge_type not in self.knowledge_base:
            self.knowledge_base[knowledge_type] = []
        
        self.knowledge_base[knowledge_type].append({
            'data': data,
            'source': sender,
            'timestamp': message_data['timestamp']
        })
        
        # Chiama il metodo specifico dell'agente per processare
        self.on_knowledge_received(knowledge_type, data, sender)
    
    def on_knowledge_received(self, knowledge_type, data, sender):
        """
        Override questo metodo negli agenti specifici per reagire alla conoscenza ricevuta
        
        Args:
            knowledge_type (str): Tipo di conoscenza ricevuta
            data (dict): Dati ricevuti
            sender (str): ID dell'agente mittente
        """
        print(f"[{self.agent_id}] Processando {knowledge_type} da {sender}: {data}")
    
    def stop(self):
        """Ferma l'agente e chiude le connessioni"""
        self.active = False
        if self.redis_client:
            self.redis_client.close()
        print(f"[{self.agent_id}] Agente fermato")
    
    @abstractmethod
    def process(self):
        """Logica principale dell'agente - da implementare nelle sottoclassi"""
        pass
    
    @abstractmethod
    def get_capabilities(self):
        """Restituisce le capacità dell'agente - da implementare nelle sottoclassi"""
        pass