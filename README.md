# MIA - Machine Intelligence Amplification Framework

Questo repository contiene il codice sorgente per il progetto MIA, un framework agentico sperimentale progettato per l'amplificazione dell'intelligenza artificiale attraverso il ragionamento simbolico e l'interazione con sistemi computazionali esterni.

L'obiettivo finale di questo progetto è esplorare architetture di IA in grado di superare i limiti tradizionali, con una prima "missione" focalizzata sulla dimostrazione del **Teorema Universale della Soglia per la Correzione di Errori Quantistici**.

## Setup dell'Ambiente di Sviluppo

Questo progetto è sviluppato all'interno di WSL (Windows Subsystem for Linux) e gestito tramite Conda.

### Routine di Avvio Rapido

Per iniziare a lavorare, seguire questi passi:

1.  **Aprire il progetto in VS Code (connesso a WSL)**:
    * Avviare VS Code.
    * Usare la funzione `File > Apri Recenti...` per selezionare la cartella `MIA` o connettersi a WSL (`Ctrl+Shift+P` -> `WSL: Connect to WSL`) e aprire la cartella del progetto (`/percorso/alla/tua/cartella/MIA`).

2.  **Aprire un terminale integrato in VS Code**:
    * Usare la scorciatoia `Ctrl+` o il menu `Terminale > Nuovo Terminale`.

3.  **Attivare l'ambiente Conda**:
    * Eseguire il seguente comando nel terminale integrato:
        ```bash
        conda activate mia_env
        ```

L'ambiente è ora pronto. Il prompt del terminale dovrebbe iniziare con `(mia_env)`.