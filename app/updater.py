from app.database import Database


class TransactionUpdater:

    def __init__(self):

        self.db = Database()


    def update_prediction(
        self,
        comp_cd,
        branch_cd,
        tran_cd,
        tran_dt,
        prediction,
        anomaly_score
    ):

        conn = None
        cursor = None


        try:

            conn = self.db.connect()

            cursor = conn.cursor()


            query = """
            UPDATE daily_trn
            SET

                fraud_prediction = %s,

                fraud_score = %s,

                verified_by_ml = 'Y',

                ml_verified_time = CURRENT_TIMESTAMP


            WHERE

                TRIM(comp_cd) = %s

                AND TRIM(branch_cd) = %s

                AND tran_cd = %s

                AND DATE(tran_dt) = %s::date
            """


            cursor.execute(

                query,

                (

                    prediction,

                    round(
                        float(anomaly_score),
                        6
                    ),


                    comp_cd.strip(),

                    branch_cd.strip(),

                    tran_cd,

                    tran_dt

                )

            )


            rows_updated = cursor.rowcount


            conn.commit()



            if rows_updated == 0:

                print(
                    "Warning: No transaction updated"
                )

            else:

                print(
                    f"Transaction updated successfully. Rows: {rows_updated}"
                )



        except Exception as e:


            if conn:

                conn.rollback()


            print(
                "Update Error:",
                e
            )



        finally:


            if cursor:

                cursor.close()


            if conn:

                conn.close()