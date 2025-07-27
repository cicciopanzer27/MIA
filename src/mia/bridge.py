# src/mia/bridge.py (versione ottimizzata)

import subprocess
import json
import threading
import queue
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import redis

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LEIN_COMMAND = "lein"

@dataclass
class SimulationRequest:
    """Richiesta di simulazione verso il core Clojure"""
    simulator_type: str
    target_system: Dict[str, Any]
    # ... altri campi se necessario

class ClojureBridge:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ClojureBridge, cls).__new__(cls)
        return cls._instance

    def __init__(self, clojure_project_path: str = "./", redis_host: str = "localhost", redis_port: int = 6379):
        if hasattr(self, 'initialized'):
            return
        with self._lock:
            if hasattr(self, 'initialized'):
                return

            self.clojure_path = Path(clojure_project_path)
            self.process = None
            self.reader_thread = None
            self.output_queue = queue.Queue()
            self.request_futures = {} # Per tracciare le risposte

            self.start_clojure_process()

            try:
                self.redis_client = redis.Redis(host=redis_host, port=redis_port)
                self.redis_client.ping()
                logger.info("✅ Connessione Redis stabilita")
            except Exception as e:
                logger.error(f"❌ Errore connessione Redis: {e}")
                raise

            self.initialized = True
            logger.info("🌉 Bridge Python-Clojure inizializzato e operativo.")

    def start_clojure_process(self):
        """Avvia il kernel Clojure come processo persistente."""
        if self.process and self.process.poll() is None:
            logger.warning("Il processo Clojure è già in esecuzione.")
            return

        try:
            logger.info(f"Avvio del kernel Clojure dal percorso: {self.clojure_path.resolve()}")
            self.process = subprocess.Popen(
                [LEIN_COMMAND, "run", "-m", "mia.core"],
                cwd=str(self.clojure_path.resolve()),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            self.reader_thread = threading.Thread(target=self._enqueue_output, daemon=True)
            self.reader_thread.start()
            
            error_thread = threading.Thread(target=self._log_stderr, daemon=True)
            error_thread.start()

            # Attendi il messaggio di 'ready' dal kernel
            try:
                initial_response = self.output_queue.get(timeout=30)
                if json.loads(initial_response).get("status") != "ready":
                    raise RuntimeError("Il kernel Clojure non si è avviato correttamente.")
                logger.info("✅ Kernel Clojure pronto e in ascolto.")
            except (queue.Empty, json.JSONDecodeError) as e:
                logger.error(f"Nessuna risposta di 'ready' dal kernel Clojure. Errore: {e}")
                self.shutdown()
                raise RuntimeError("Impossibile inizializzare il kernel Clojure.")

        except FileNotFoundError:
            logger.error(f"ERRORE CRITICO: Comando '{LEIN_COMMAND}' non trovato.")
            raise
        except Exception as e:
            logger.error(f"ERRORE CRITICO nell'avvio del processo Clojure: {e}")
            raise

    def _enqueue_output(self):
        """Legge l'output JSON da stdout e lo mette in una coda o abbina alle richieste."""
        for line in iter(self.process.stdout.readline, ''):
            try:
                response = json.loads(line)
                request_id = response.get("request_id")
                if request_id in self.request_futures:
                    future = self.request_futures.pop(request_id)
                    future.put(response)
                else:
                    # Per output non richiesti o broadcast
                    self.output_queue.put(response)
            except json.JSONDecodeError:
                logger.warning(f"Output non-JSON ricevuto da Clojure: {line.strip()}")

    def _log_stderr(self):
        """Logga l'output di errore dal processo Clojure."""
        for line in iter(self.process.stderr.readline, ''):
            logger.error(f"[Clojure Kernel] {line.strip()}")

    def _send_request(self, command: str, payload: Dict, timeout: int = 30) -> Dict:
        """Invia una richiesta al kernel e attende una risposta specifica."""
        request_id = f"req_{int(time.time() * 1000)}"
        
        request = {
            "request_id": request_id,
            "command": command,
            "payload": payload
        }
        
        future = queue.Queue()
        self.request_futures[request_id] = future
        
        try:
            self.process.stdin.write(json.dumps(request) + '\n')
            self.process.stdin.flush()
            
            # Attendi la risposta
            response = future.get(timeout=timeout)
            if "error" in response:
                logger.error(f"Errore dal kernel per la richiesta {request_id}: {response['error']}")
            return response.get("result", {"error": "Nessun risultato nella risposta"})

        except queue.Empty:
            logger.error(f"Timeout in attesa della risposta per la richiesta {request_id}")
            self.request_futures.pop(request_id, None)
            return {"error": "Timeout"}
        except Exception as e:
            logger.error(f"Errore durante l'invio della richiesta {request_id}: {e}")
            self.request_futures.pop(request_id, None)
            return {"error": str(e)}

    # --- API PUBBLICHE (esempi) ---
    def simulate_molecule(self, atoms: List[str], conditions: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"🧪 Simulazione molecolare: {'-'.join(atoms)}")
        payload = {"atoms": atoms, "conditions": conditions}
        return self._send_request("simulate-molecule", payload)

    def symbolic_inference(self, premise: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"🧠 Inferenza simbolica: {premise[:50]}...")
        payload = {"premise": premise, "context": context}
        return self._send_request("symbolic-inference", payload)

    def health_check(self) -> Dict[str, Any]:
        return self._send_request("health-check", {})

    def shutdown(self):
        logger.info("🔄 Shutdown bridge in corso...")
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
        logger.info("✅ Bridge shutdown completato")

# Mantieni la tua classe SymbolicBridge che eredita da questa
class SymbolicBridge(ClojureBridge):
    pass
