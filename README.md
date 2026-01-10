# simesamesac

## 1. Configurazione Ambiente Locale Python

Crea e attiva un ambiente virtuale per isolare le dipendenze del progetto.

```bash
# Crea l'ambiente virtuale
python3 -m venv venv

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

```

---

## 2. Inizializzazione Google Cloud CLI

Assicurati che i componenti necessari per App Engine siano installati e aggiornati.

```bash
# Aggiorna i componenti
gcloud components update

# Installa il supporto per App Engine Python
gcloud components install app-engine-python

# Effettua il login (se non già loggato)
gcloud auth login

```

---

## 3. Configurazione Progetto GCP

Sostituisci `IL_TUO_PROJECT_ID` con l'ID univoco che desideri.

```bash
# Definizione variabili d'ambiente
export NAME=webuser
export PROJECT_ID=IL_TUO_PROJECT_ID

# Creazione del progetto e impostazione come default
gcloud projects create ${PROJECT_ID} --set-as-default

# Verifica se il progetto è impostato correttamente
gcloud config set project ${PROJECT_ID}

# Abilitazione dei servizi necessari
gcloud services enable \
  appengine.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com

```

---

## 4. Creazione App Engine e Firestore

L'applicazione App Engine deve essere creata prima di procedere al deploy.

```bash
# Inizializza l'applicazione App Engine (scegli la regione quando richiesto)
gcloud app create --project=${PROJECT_ID}

# Verifica lo stato del progetto
gcloud projects list
gcloud projects describe ${PROJECT_ID}

```

---

## 5. Gestione Credenziali (Service Account)

Configurazione dei permessi per permettere all'applicazione di accedere ai servizi GCP.

```bash
# Crea il Service Account
gcloud iam service-accounts create ${NAME} --project=${PROJECT_ID}

# Assegna il ruolo di Owner al Service Account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role "roles/owner"

# Genera il file delle chiavi JSON
gcloud iam service-accounts keys create credentials.json \
  --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# Esporta la variabile d'ambiente per le credenziali (per test locali)
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"

```

---

## 6. Comandi di Debug Utili

In caso di errori di configurazione del progetto:

```bash
# Mostra il progetto attualmente attivo
gcloud config list project

# Forza il cambio progetto se non aggiornato
gcloud config set project ${PROJECT_ID}

```

---

## 7. Deploy dell'Applicazione

Una volta completata la configurazione, carica l'app online.

```bash
# Deploy su App Engine
gcloud app deploy app.yaml

# Apri l'app nel browser
gcloud app browse

```

---

**Suggerimento per GitHub:** Se vuoi che `credentials.json` non venga caricato sul server (per sicurezza), ricordati di aggiungerlo al file `.gitignore`.

Vuoi che aggiunga anche una sezione specifica su come configurare **Firestore** in modalità Native o Datastore?
