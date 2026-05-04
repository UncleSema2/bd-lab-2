import configparser
import os
import pickle
import numpy as np
from fastapi import APIRouter, HTTPException

from src.api.schemas import PredictRequest, PredictResponse

router = APIRouter()

MODELS = ["LOG_REG"]

_config = configparser.ConfigParser()
_config.read("config.ini")

_classifiers: dict = {}
_scaler = None


def _load_artifacts():
    global _scaler
    if _scaler is None:
        scaler_path = _config["SPLIT_DATA"]["scaler"]
        try:
            with open(scaler_path, "rb") as f:
                _scaler = pickle.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=503, detail="Scaler is not trained yet")
    for name in MODELS:
        if name not in _classifiers:
            path = _config[name]["path"]
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    _classifiers[name] = pickle.load(f)


@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if request.model not in MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}")
    _load_artifacts()
    if request.model not in _classifiers:
        raise HTTPException(
            status_code=503, detail=f"Model {request.model} not trained yet"
        )
    try:
        X = np.array(request.features).reshape(1, -1)
        X_scaled = _scaler.transform(X)
        prediction = int(_classifiers[request.model].predict(X_scaled)[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid features: {e}")
    return PredictResponse(prediction=prediction, model=request.model)
