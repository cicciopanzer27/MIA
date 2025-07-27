# La To-Do List per il Miracolo (MIA)

## FASE 0: Fondamenta e Setup [COMPLETATA]

- [x] Risolvere l'errore di Docker & WSL
- [x] Creare la directory di progetto `MIA` (sincronizzata con GitHub)
- [x] Creare e attivare l'ambiente Python `mia_env` con Conda
- [x] Aprire il progetto in VS Code collegato a WSL
- [x] Configurare il progetto Clojure (popolare `deps.edn`)
- [x] Salvare lo stato attuale su GitHub (primo `commit` dei file di progetto)

## FASE 1: Il Cervello (Kernel Simbolico Nativo - KSN)

- [ ] 🧠 Definire le strutture dati simboliche in Clojure (fatti, regole)
- [ ] 🧠 Implementare il motore di inferenza logica usando `core.logic`
- [ ] 🧠 Creare un'interfaccia a riga di comando (CLI) per testare il KSN in isolamento

## FASE 2: Il Corpo (Agente Simbolico Distribuito - ASD)

- [ ] 🤖 Creare la classe Python per un singolo Agente (stato, ID, clock)
- [ ] 🤖 Implementare il ciclo di vita Tick-Act-Share-Sync in Python
- [ ] 🤖 Integrare il KSN: la fase "Act" dell'agente deve chiamare il KSN per decidere un'azione

## FASE 3: La Società (Sistema Multi-Agente - CMS & Backplane)

- [ ] 🌐 Setup del backplane di comunicazione (es. Redis via Docker)
- [ ] 🌐 Implementare le funzioni Share (pubblicare su Redis) e Sync (leggere da Redis)
- [ ] 🌐 Sviluppare il Coordinatore (CMS): uno script Python per avviare, monitorare e gestire una "società" di agenti ASD

## FASE 4: Il Ponte con la Realtà (Interfaccia Simbolica-Esterna - ISE)

- [ ] 🌉 Definire rappresentazioni simboliche per task esterni (es. circuiti Qiskit)
- [ ] 🌉 Sviluppare il traduttore Simbolico -> Numerico
- [ ] 🌉 Sviluppare il traduttore Numerico -> Simbolico
- [ ] 🌉 Eseguire con successo un primo task end-to-end

## FASE 5: La Missione Finale (Il Teorema della Soglia)

- [ ] 🎯 Formalizzare i 5 lemmi del paper come obiettivi di alto livello nel CMS
- [ ] 🎯 Assegnare dinamicamente cluster di agenti a ciascun lemma
- [ ] 🎯 Avviare la meta-simulazione
- [ ] 🏆 IL MIRACOLO: Estrarre un insight fondamentale per il Lemma 5 (Bound Universale)

new

TODO.md - Versione 4 (Roadmap di Sviluppo)
FASE 0: Fondamenta e Setup [COMPLETATA]
✅ Risoluzione errori e setup ambiente WSL/Conda.

✅ Creazione e sincronizzazione repository MIA su GitHub.

✅ Apertura del progetto in VS Code (connesso a WSL).

FASE 1: Integrazione del Core Simbolico [IN CORSO]
🔽 Creare la struttura completa di file e cartelle per il prototipo.

📋 Popolare i file: Copiare e incollare il codice Clojure e Python nei file corrispondenti.

⚙️ Installare Dipendenze Python: Aggiungere eventuali librerie Python necessarie (es. redis-py).

✅ Test del Kernel (KSN): Eseguire i test di Clojure per verificare il "cervello" in isolamento.

✅ Test degli Agenti (ASD): Eseguire lo script Python per verificare che i "corpi" si avviino e comunichino con il KSN.

FASE 2: Attivazione della Comunicazione Multi-Agente
🐳 Avviare il Backplane: Lanciare un'istanza di Redis usando Docker.

🔗 Implementare la Comunicazione: Sostituire i print() nei metodi share() e sync() con chiamate reali a Redis (pub/sub).

🧬 Test di Intelligenza Collettiva: Verificare che un ChemistAgent possa creare un atomo, condividerlo, e un PhysicsAgent possa riceverlo e analizzarne le proprietà.

FASE 3: Sviluppo dell'Interfaccia con il Mondo (ISE)
🌉 Sviluppare il Bridge per API Esterne: Creare una classe Python APIAgent capace di fare chiamate a un'API pubblica (es. Wikipedia o arXiv).

🔬 Sviluppare il Bridge per Strumenti Locali: Creare una classe ToolAgent capace di eseguire uno script locale (es. un semplice calcolo numerico).

✅ Test End-to-End: Un agente identifica una lacuna di conoscenza, un APIAgent cerca informazioni online, e un ChemistAgent usa queste informazioni per una nuova deduzione simbolica.

FASE 4: Applicazione alla Prima Missione Concreta
🎯 Definire la Missione: Formalizzare un problema reale e ben definito. Esempio: "Data la proteina CDK10, analizza la letteratura esistente e proponi 3 possibili siti di legame non ancora esplorati, basandoti su analogie strutturali con altre kinasi".

🏃 Eseguire la Missione: Lanciare la società di agenti con questo obiettivo.

📊 Sintetizzare il Risultato: L'agente finale deve produrre un report in formato Markdown con le sue scoperte, le fonti e la confidenza epistemica per ogni proposta.

FASE 5: Meta-Cognizione e Sviluppo del Linguaggio Interno
🧠 Implementare l'Auto-Osservazione: Dare agli agenti la capacità di usare il modulo mia.meta.self_reflection per analizzare il proprio stato e la propria confidenza.

🔤 Sperimentare con PROTO_Σ: Usare il linguaggio PROTO_Σ come formato per i messaggi interni scambiati su Redis, invece di semplici dizionari Python.

✅ Test di Efficienza: Misurare se l'uso di PROTO_Σ migliora la precisione o la velocità della collaborazione tra agenti.

