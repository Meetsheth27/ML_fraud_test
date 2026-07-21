from app.predictor import FraudPredictor


predictor = FraudPredictor()


transaction = {

    "amount": 5000000,

    "branch_cd": "099",

    "through_channel": "UPI",

    "acct_type": "CURRENT",

    "tran_dt": "2026-07-21 03:00:00"

}


result = predictor.predict(transaction)


print(result)