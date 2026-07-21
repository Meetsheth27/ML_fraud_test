from app.model_loader import ModelLoader
from app.features import FeatureExtractor


class FraudPredictor:

    def __init__(self):

        self.model = ModelLoader().get_model()

        self.extractor = FeatureExtractor()


    def predict(self, transaction):

        """
        Predict fraud for a single transaction.

        transaction example:

        {
            "amount":500000,
            "branch_cd":"BR001",
            "through_channel":"ATM",
            "acct_type":"SAV",
            "tran_dt":"2026-01-22 03:00:00"
        }

        """


        # ------------------------------------------
        # Feature Extraction
        # ------------------------------------------

        features = self.extractor.extract(
            transaction
        )


        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        prediction_result = (
            self.model
            .predict(features)[0]
        )


        # ------------------------------------------
        # Anomaly Score
        # ------------------------------------------

        anomaly_score = (
            self.model
            .decision_function(features)[0]
        )


        # ------------------------------------------
        # Convert Result
        # ------------------------------------------

        if prediction_result == -1:

            prediction = "FRAUD"

        else:

            prediction = "NORMAL"


        return {

            "fraud_prediction": prediction,

            # Original Isolation Forest output
            "model_result": int(prediction_result),

            # Negative means suspicious
            "anomaly_score": round(
                float(anomaly_score),
                6
            )

        }