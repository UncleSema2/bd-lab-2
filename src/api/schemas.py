from pydantic import BaseModel, Field
from typing import List


class PredictRequest(BaseModel):
    features: List[float] = Field(..., min_length=30, max_length=30)
    model: str = "LOG_REG"


class PredictResponse(BaseModel):
    prediction: int
    model: str
