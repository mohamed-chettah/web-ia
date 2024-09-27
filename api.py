from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, LogisticRegression
import uvicorn
import numpy as np
import pandas as pd
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de prédiction
note_model = LinearRegression()
year_model = LinearRegression()
garage_model = LogisticRegression()

# Vérification d'entraînement des modèles
is_note_model_trained = False
is_year_model_trained = False
is_garage_model_trained = False

# Schéma de données pour les prédictions
class NotePredictionData(BaseModel):
    surface: float
    prix: float
    ville: str

class YearPredictionData(BaseModel):
    ville: str

class GaragePredictionData(BaseModel):
    prix: float
    ville: str

class Bien(BaseModel):
    surface: float
    prix: float
    ville: str
    note: float
    annee: int
    garage: bool

CSV_FILE_PATH = 'C:/ESGI/derniere-annee/web-ia/web-ia/biens.csv'

# Récupérer la liste des biens
@app.get("/biens", response_model=list[Bien])
async def get_biens():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        
        # Conversion du dataframe en liste de dictionnaires
        biens = df.to_dict(orient="records")
        
        # Retourner la liste des biens
        return biens
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des biens: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des biens.")

@app.post("/biens")
async def add_bien(bien: Bien):
    # Vérifier si le fichier CSV existe
    file_exists = os.path.isfile(CSV_FILE_PATH)

    try:
        # Charger les données existantes s'il y en a
        if file_exists:
            df = pd.read_csv(CSV_FILE_PATH)
        else:
            # Créer un DataFrame vide avec les bonnes colonnes si le fichier n'existe pas
            df = pd.DataFrame(columns=["surface", "prix", "ville", "note", "annee", "garage"])

        # Ajouter le nouveau bien sous forme de dictionnaire
        new_bien = pd.DataFrame([{
            "surface": bien.surface,
            "prix": bien.prix,
            "ville": bien.ville,
            "note": bien.note,
            "annee": bien.annee,
            "garage": bien.garage
        }])

        # Concaténer le nouveau bien au DataFrame
        df = pd.concat([df, new_bien], ignore_index=True)

        # Sauvegarder le DataFrame mis à jour dans le fichier CSV
        df.to_csv(CSV_FILE_PATH, index=False)

        return {"message": "Bien ajouté avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout du bien: {e}")

# Entraînement du modèle de prédiction de la note
@app.post("/train-note")
async def train_note_model():
    global is_note_model_trained
    df = pd.read_csv(CSV_FILE_PATH)
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['surface', 'prix', 'ville_encoded']]
    y = df['note']
    note_model.fit(X, y)
    is_note_model_trained = True
    return {"message": "Modèle de prédiction de la note entraîné."}

# Prédiction de la note
@app.post("/predict-note")
async def predict_note(data: NotePredictionData):
    if not is_note_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")

    ville_clean = data.ville.strip().lower()
    ville_mapping = {'paris': 0, 'lyon': 1, 'marseille': 2}

    if ville_clean not in ville_mapping:
        raise HTTPException(status_code=400, detail=f"Ville '{data.ville}' non supportée.")

    ville_encoded = ville_mapping[ville_clean]
    X_new = np.array([[data.surface, data.prix, ville_encoded]])
    
    predicted_note = note_model.predict(X_new)[0]
    return {"predicted_note": predicted_note}


# Entraînement du modèle de prédiction de l'année
@app.post("/train-year")
async def train_year_model():
    global is_year_model_trained
    df = pd.read_csv(CSV_FILE_PATH)
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['ville_encoded']]
    y = df['annee']
    year_model.fit(X, y)
    is_year_model_trained = True
    return {"message": "Modèle de prédiction de l'année entraîné."}

# Prédiction de l'année
@app.post("/predict-year")
async def predict_year(data: YearPredictionData):
    if not is_year_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")

    ville_clean = data.ville.strip().lower()
    ville_mapping = {'paris': 0, 'lyon': 1, 'marseille': 2}

    if ville_clean not in ville_mapping:
        raise HTTPException(status_code=400, detail=f"Ville '{data.ville}' non supportée.")

    ville_encoded = ville_mapping[ville_clean]
    X_new = np.array([[ville_encoded]])
    predicted_year = year_model.predict(X_new)[0]

    return {"predicted_year": predicted_year}

# Entraînement du modèle de prédiction du garage
@app.post("/train-garage")
async def train_garage_model():
    global is_garage_model_trained
    df = pd.read_csv(CSV_FILE_PATH)
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['prix', 'ville_encoded']]
    y = df['garage']
    garage_model.fit(X, y)
    is_garage_model_trained = True
    return {"message": "Modèle de prédiction du garage entraîné."}

# Prédiction du garage
@app.post("/predict-garage")
async def predict_garage(data: GaragePredictionData):
    if not is_garage_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")

    ville_clean = data.ville.strip().lower()
    ville_mapping = {'paris': 0, 'lyon': 1, 'marseille': 2}

    if ville_clean not in ville_mapping:
        raise HTTPException(status_code=400, detail=f"Ville '{data.ville}' non supportée.")

    ville_encoded = ville_mapping[ville_clean]
    X_new = np.array([[data.prix, ville_encoded]])
    has_garage = garage_model.predict(X_new)[0]
    return {"has_garage": bool(has_garage)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5001)
