import numpy as np
import pandas as pd


class FeatureExtractor:

    def extract(self, transaction):

        # Convert transaction into dataframe
        df = pd.DataFrame(
            [transaction]
        )


        # -----------------------------
        # Amount Feature
        # -----------------------------

        df["amount"] = (
            df["amount"]
            .fillna(0)
            .astype(float)
        )


        # Same feature used during training

        df["amount_log"] = (
            np.log1p(
                df["amount"]
            )
        )


        # -----------------------------
        # Transaction Date Features
        # -----------------------------

        df["tran_dt"] = pd.to_datetime(
            df["tran_dt"]
        )


        df["tran_hour"] = (
            df["tran_dt"]
            .dt.hour
        )


        df["day_of_week"] = (
            df["tran_dt"]
            .dt.dayofweek
        )


        # Remove timestamp

        df.drop(
            columns=["tran_dt"],
            inplace=True
        )


        # -----------------------------
        # Categorical Features
        # -----------------------------

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


        # IMPORTANT:
        # Keep exactly same columns
        # and order as training

        return df[
            [
                "amount",
                "amount_log",
                "tran_hour",
                "day_of_week",
                "branch_cd",
                "through_channel",
                "acct_type"
            ]
        ]