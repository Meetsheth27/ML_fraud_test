import os
import joblib
import numpy as np
import pandas as pd

from sqlalchemy import create_engine

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from app.config import Config


# --------------------------------------------------
# PostgreSQL Connection
# --------------------------------------------------

DATABASE_URL = (
    f"postgresql://{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"
)


engine = create_engine(DATABASE_URL)


# --------------------------------------------------
# Load Historical Transactions
# --------------------------------------------------

query = """
SELECT
    amount,
    branch_cd,
    through_channel,
    acct_type,
    tran_dt
FROM daily_trn
"""


print("Loading transaction data...")


df = pd.read_sql(
    query,
    engine
)


print("Loaded rows:", len(df))


# --------------------------------------------------
# Data Cleaning
# --------------------------------------------------

print("Cleaning transaction data...")


# Remove invalid amounts

df = df[
    (df["amount"] > 0)
    &
    (df["amount"] < 10000000)
]


print(
    "Rows after amount filtering:",
    len(df)
)


# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

print("Creating features...")


# Convert timestamp safely

df["tran_dt"] = pd.to_datetime(
    df["tran_dt"],
    errors="coerce"
)


# Extract hour

df["tran_hour"] = (
    df["tran_dt"]
    .dt.hour
)


# Extract day

df["day_of_week"] = (
    df["tran_dt"]
    .dt.dayofweek
)


# Handle missing dates

df["tran_hour"] = (
    df["tran_hour"]
    .fillna(-1)
)


df["day_of_week"] = (
    df["day_of_week"]
    .fillna(-1)
)


# Remove timestamp

df.drop(
    columns=["tran_dt"],
    inplace=True
)



# --------------------------------------------------
# Missing Values
# --------------------------------------------------

df["amount"] = (
    df["amount"]
    .fillna(0)
)


df["branch_cd"] = (
    df["branch_cd"]
    .fillna("UNKNOWN")
    .astype(str)
)


df["through_channel"] = (
    df["through_channel"]
    .fillna("UNKNOWN")
    .astype(str)
)


df["acct_type"] = (
    df["acct_type"]
    .fillna("UNKNOWN")
    .astype(str)
)



# --------------------------------------------------
# Additional Fraud Feature
# --------------------------------------------------

df["amount_log"] = (
    np.log1p(df["amount"])
)



# --------------------------------------------------
# Features
# --------------------------------------------------

numeric_features = [

    "amount",

    "amount_log",

    "tran_hour",

    "day_of_week"
]


categorical_features = [

    "branch_cd",

    "through_channel",

    "acct_type"
]



# --------------------------------------------------
# Preprocessing Pipeline
# --------------------------------------------------

preprocessor = ColumnTransformer(

    transformers=[

        (
            "numeric",

            StandardScaler(),

            numeric_features
        ),


        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        )
    ]
)



# --------------------------------------------------
# Isolation Forest Model
# --------------------------------------------------

model = IsolationForest(

    n_estimators=300,

    contamination=0.05,

    random_state=42

)



# --------------------------------------------------
# Complete Pipeline
# --------------------------------------------------

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",

            preprocessor
        ),


        (
            "model",

            model
        )
    ]

)



# --------------------------------------------------
# Train Model
# --------------------------------------------------

print(
    "Training fraud detection model..."
)


pipeline.fit(df)



# --------------------------------------------------
# Check Model Performance
# --------------------------------------------------

print(
    "\nChecking model output..."
)


predictions = (
    pipeline.predict(df)
)


print(
    "\nPrediction Distribution:"
)


print(
    pd.Series(predictions)
    .value_counts()
)



scores = (
    pipeline
    .decision_function(df)
)


print(
    "\nAnomaly Score Range:"
)


print(
    "Minimum:",
    scores.min()
)


print(
    "Maximum:",
    scores.max()
)



# --------------------------------------------------
# Save Model
# --------------------------------------------------

os.makedirs(
    "models",
    exist_ok=True
)



model_path = (

    Config.MODEL_PATH

    if Config.MODEL_PATH

    else "models/fraud_model.pkl"

)



joblib.dump(

    pipeline,

    model_path

)



print("--------------------------------")
print("Fraud model trained successfully")
print("Saved at:", model_path)
print("--------------------------------")