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