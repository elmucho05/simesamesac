`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

# Initialize Google Cloud CLI if not done yet
`gcloud components update`
`gcloud components install app-engine-python`

## If still not logged in
`gcloud auth login`

# Enable building project
`gcloud services enable appengine.googleapis.com cloudbuild.googleapis.com storage.googleapis.com`

# Creating project
`export NAME=webuser`
`export PROJECT_ID=`
`gcloud projects create ${PROJECT_ID} --set-as-default` 

## Se il progetto non e' impostato come default:
  `gcloud config set project ${PROJECT_ID}`

# Lista progetti
`gcloud projects list`
`gcloud projects describe ${PROJECT_ID}`

# POI, CREARE L'APP
`gcloud app create --project=${PROJECT_ID}`


# if errors for old projects
  gcloud config list project

# SETUP DELLE CREDENZIALI
`gcloud iam service-accounts create ${NAME}`
`gcloud iam service-accounts create ${NAME} --project=${PROJECT_ID}`

# if errors

`gcloud projects create ${PROJECT_ID} --set-as-default` 
if not deafult : `gcloud config set project $PROJECT_ID`

### LINK BILLING
# THEN
`gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"`


`touch credentials.json`

`gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com`


`export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"`
