from fastapi import FastAPI
from pydantic import BaseModel
from ml_model import sentinel_model, predict_fraud_probability

app = FastAPI(title="AM Graph Sentinel API", description="Fraud Prediction API")

class Transaction(BaseModel):
    transaction_amount: float
    transaction_hour: int
    geo_risk_score: float
    device_auth_score: float
    frequency: int

class Prediction(BaseModel):
    fraud_probability: float
    is_fraud: bool

@app.get("/")
def read_root():
    return {"message": "AM Graph Sentinel API is running"}

@app.post("/predict", response_model=Prediction)
def predict(transaction: Transaction):
    probability = predict_fraud_probability(
        sentinel_model,
        transaction.transaction_amount,
        transaction.transaction_hour,
        transaction.geo_risk_score,
        transaction.device_auth_score,
        transaction.frequency
    )
    
    return Prediction(
        fraud_probability=float(probability),
        is_fraud=bool(probability > 0.5)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
