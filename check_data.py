import pandas as pd
from sqlalchemy import create_engine

from app.config import Config


DATABASE_URL = (
    f"postgresql://{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"
)


engine = create_engine(DATABASE_URL)


df = pd.read_sql(
    """
    SELECT
        amount,
        branch_cd,
        through_channel,
        acct_type,
        tran_dt
    FROM daily_trn
    """,
    engine
)


print(df["amount"].describe())


print("\nMaximum amount:")
print(
    df["amount"].max()
)


print("\nLargest transactions:")
print(
    df.sort_values(
        "amount",
        ascending=False
    ).head(10)
)