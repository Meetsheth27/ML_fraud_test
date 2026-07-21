import select

from app.database import Database
from app.logger import logger
from app.repository import TransactionRepository
from app.predictor import FraudPredictor
from app.updater import TransactionUpdater


class TransactionListener:

    def __init__(self):

        self.db = Database()

        self.repo = TransactionRepository()

        self.predictor = FraudPredictor()

        self.updater = TransactionUpdater()



    def start(self):

        print("Starting Transaction Listener...")


        conn = self.db.connect()

        cursor = conn.cursor()


        # Listen to PostgreSQL notification channel

        cursor.execute(
            "LISTEN new_transaction;"
        )


        print(
            "Listening on channel : new_transaction"
        )


        logger.info(
            "Listening on channel : new_transaction"
        )



        while True:


            if select.select(
                [conn],
                [],
                [],
                5
            ) == ([], [], []):

                continue



            conn.poll()



            while conn.notifies:


                notify = conn.notifies.pop(0)


                payload = notify.payload



                logger.info(
                    f"Notification Received : {payload}"
                )



                try:


                    # Payload format:
                    # comp_cd|branch_cd|tran_cd|tran_dt


                    comp_cd, branch_cd, tran_cd, tran_dt = (
                        payload.split("|")
                    )



                    print("\n" + "=" * 70)

                    print(
                        "NEW TRANSACTION RECEIVED"
                    )

                    print("=" * 70)



                    print(
                        f"Company Code : {comp_cd}"
                    )

                    print(
                        f"Branch Code  : {branch_cd}"
                    )

                    print(
                        f"Tran Code    : {tran_cd}"
                    )

                    print(
                        f"Tran Date    : {tran_dt}"
                    )



                    # -----------------------------------
                    # Fetch Transaction
                    # -----------------------------------


                    transaction = self.repo.get_transaction(

                        comp_cd.strip(),

                        branch_cd.strip(),

                        int(tran_cd),

                        tran_dt

                    )



                    if transaction is None:


                        print(
                            "Transaction not found"
                        )


                        logger.error(
                            "Transaction not found."
                        )


                        continue



                    print("\n" + "=" * 70)

                    print(
                        "TRANSACTION FETCHED"
                    )

                    print("=" * 70)



                    for key, value in transaction.items():

                        print(
                            f"{key:25} : {value}"
                        )



                    # -----------------------------------
                    # Fraud Prediction
                    # -----------------------------------


                    print("\n" + "=" * 70)

                    print(
                        "RUNNING FRAUD DETECTION MODEL"
                    )

                    print("=" * 70)



                    result = self.predictor.predict(
                        transaction
                    )



                    prediction = (

                        result["fraud_prediction"]

                    )


                    model_result = (

                        result["model_result"]

                    )


                    anomaly_score = (

                        result["anomaly_score"]

                    )



                    print(
                        f"Prediction      : {prediction}"
                    )


                    print(
                        f"Model Result    : {model_result}"
                    )


                    print(
                        f"Anomaly Score   : {anomaly_score}"
                    )



                    # -----------------------------------
                    # Update Database
                    # -----------------------------------


                    print(
                        "\nUpdating database..."
                    )



                    self.updater.update_prediction(

                        comp_cd.strip(),

                        branch_cd.strip(),

                        int(tran_cd),

                        tran_dt,

                        prediction,

                        anomaly_score

                    )



                    print(
                        "Database Updated Successfully."
                    )


                    print("=" * 70)


                    print(
                        "Waiting for next transaction..."
                    )


                    print("=" * 70)



                except Exception as e:


                    logger.exception(e)



                    print(
                        "Processing Error:",
                        e
                    )





# --------------------------------------------------
# Application Entry Point
# --------------------------------------------------

if __name__ == "__main__":


    listener = TransactionListener()


    listener.start()