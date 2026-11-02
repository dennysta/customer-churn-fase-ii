
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# Ruta de la carpeta del proyecto
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "modelos"

# Cargar modelos
modelo_lr = joblib.load(
    MODELS_DIR / "modelo_LogisticRegression.joblib"
)

modelo_rf = joblib.load(
    MODELS_DIR / "modelo_RandomForest.joblib"
)

app = FastAPI(
    title="Customer Churn API",
    description="API para predecir la posible cancelación de clientes.",
    version="1.0.0"
)


class Cliente(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Customer Churn API activa"
    }


@app.post("/predict")
def predict(cliente: Cliente, modelo: str = "logistic_regression"):

    if modelo == "logistic_regression":
        model = modelo_lr
    elif modelo == "random_forest":
        model = modelo_rf
    else:
        raise HTTPException(
            status_code=400,
            detail="Modelo no válido. Usa logistic_regression o random_forest."
        )

    datos = pd.DataFrame([cliente.model_dump()])

    prediccion = int(model.predict(datos)[0])
    probabilidades = model.predict_proba(datos)[0]

    return {
        "modelo": modelo,
        "prediccion": prediccion,
        "resultado": (
            "Posible churn" if prediccion == 1 else "Cliente permanece"
        ),
        "probabilidad_no_churn": float(probabilidades[0]),
        "probabilidad_churn": float(probabilidades[1])
    }
