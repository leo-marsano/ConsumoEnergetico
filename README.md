# Esame Metodi Computazionali per la Fisica di Leonardo Marsano
## Consumo energetico

* [Info generali](#info-generali)
* [Descrizione script e istruzioni di esecuzione](#descrizione-script-e-istruzioni-di-esecuzione)
* [Setup](#setup)

### **Info generali**
Il progetto si divide in tre parti:
* La **prima parte** del progetto ha lo scopo di analizzare il consumo energetico della mia abitazione per 10 giorni. 
Si sono utilizzate tabelle scaricate tramite una batteria di accumulo che campiona la potenza istantanea assorbita da: *Casa*, *Rete*, *Fotovoltaico*, *Batteria*.
I dati sono campionati ogni 5 minuti e nella cartella `december/` sono presenti file *.csv* relativi ai primi 25 giorni di dicembre 2022. Poi, come richiesto, si sono analizzati soltanto quelli relativi a 10 giorni: 16-25/12/2022.
  
* La **seconda parte** del progetto consiste nello stimare teoricamente la potenza generata dai pannelli per lo stesso arco temporale ed analizzare la differenza con i dati sperimentali. Si sono utilizzate le informazioni riguardanti la posizione del sole il 20/12 per le cordinate della mia abitazione (contenute in *`december/posSun20dec.csv`*) e quelle relative alla superficie, posizione, orientamento, inclinazione ed efficienza dei pannelli per stimare la potenza della radiazione solare trasdotta dai pannelli (approssimando che il sole si sia mosso durante i 10 giorni, in media, come il 20/12).

* La **terza parte** *(opzionale)* consiste nel trovare la percentuale di autoproduzione dell'energia utilizzata dalla casa rispetto all'utilizzo totale per l'arco temporale considerato.

### **Descrizione script e istruzioni di esecuzione**
Sono stati prodotti 4 script:
* `enModule.py`: per la definizione di due classi con funzioni utili per leggere e memorizzare in oggetti i dati campionati presenti nei csv. E' importato negli altri 3 script.
* `enFunctions.py`: per la definizione di funzioni utili per ottimizzare il codice per la parte di analisi. E' importato nei prossimi 2 script.
* `enProject.py`: script con cui si memorizzano i dati campionati, analizzandoli (**prima parte**) e trovando la percentuale di autoproduzione energetica (**terza parte**) utilizzando le classi e le funzioni sovra citate (importandone i rispettivi moduli). E' importato nell'ultimo script.

  La **prima parte** si suddivide in:
  - confrontare le potenze per le diverse categorie;
  - studiare la serie temporale delle diverse categorie e dell'assorbimento totale tramite un'analisi di Fourier (caratterizzare il rumore, verificare  periodicità e correlazioni)
  - studiare l'integrale della potenza in funzione del tempo per le diverse categorie e per l'assorbimento totale;
* `enSunPanel.py`: script con cui si esegue la **seconda parte** del progetto, utilizzando i dati sperimentati memorizzati nello script precedente.

  La **seconda parte** si suddivide in:
  - stimare la potenza generata per lo stesso periodo di tempo di cui si hanno a disposizione i dati;
  - confrontare il modello di potenza generata coi dati corrispondenti;
  - effettuare una analisi di Fourier della funzione differenza fra stima teorica e dati sperimentali.
  
Per eseguire correttamente gli script basterà clonare questa repository per poi eseguire il file `enSunPanel.py`; questo, dato che importa gli altri script, eseguirà anche le altre parti del progetto. In alternativa, se si vuole eseguire soltato la parte di analisi e autoproduzione, basta eseguire il file `enProject.py`. 
Le esecuzioni produrranno e salveranno grafici che esauriscono la trattazione del progetto. Inoltre verranno printati nel terminale alcune informazioni aggiuntive per le diverse categorie riguardanti l'analisi di Fourier e le energie totali assorbite.
	
### **Setup**
Gli script importano i seguenti pacchetti Python (da installare se non presenti):
```
numpy
scipy
pandas
matplotlib
varname
```
Inoltre è necessario installare il pacchetto **`pure_eval`**, anche se non importato esplicitamente in nessuno script, onde evitare *`Warning`* in fase di esecuzione di funzioni del pacchetto **`varname`**.
