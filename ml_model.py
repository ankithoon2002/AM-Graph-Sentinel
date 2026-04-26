import numpy as np
from sklearn.ensemble import RandomForestClassifier

# --- 1. ENTERPRISE ML ENGINE (EXTENDED LOGIC) ---
# Predicting fraud based on multi-dimensional transaction features
def initialize_ml_engine():
    # Features: [Transaction_Amount, Time_Hour, Geo_Risk_Score, Device_Auth_Score, Frequency]
    training_data = np.array([
        [100, 12, 0.1, 0.9, 1], [85000, 3, 0.95, 0.2, 12],
        [450, 15, 0.05, 0.95, 2], [120000, 1, 0.98, 0.1, 25],
        [2200, 10, 0.2, 0.85, 1], [65000, 4, 0.88, 0.3, 10],
        [30, 20, 0.01, 0.99, 1], [92000, 2, 0.92, 0.15, 18]
    ])
    labels = np.array([0, 1, 0, 1, 0, 1, 0, 1])  # 0: Secure, 1: Fraudulent

    classifier = RandomForestClassifier(n_estimators=300, max_depth=15, class_weight="balanced", random_state=42)
    classifier.fit(training_data, labels)
    return classifier


def predict_fraud_probability(model, transaction_amount, transaction_hour, geo_risk_score, device_auth_score, frequency):
    """
    Returns fraud probability as a value between 0 and 1.
    """
    features = [[
        transaction_amount,
        transaction_hour,
        geo_risk_score,
        device_auth_score,
        frequency,
    ]]

    return model.predict_proba(features)[0][1]


# Global Model Instance
sentinel_model = initialize_ml_engine()
