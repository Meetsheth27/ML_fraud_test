import psycopg2.extras

from app.database import Database


class TransactionRepository:

    def __init__(self):
        self.db = Database()


    def get_transaction(
        self,
        comp_cd,
        branch_cd,
        tran_cd,
        tran_dt
    ):

        conn = None
        cursor = None

        try:

            conn = self.db.connect()

            cursor = conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )


            print("\nSearching for:")
            print(f"comp_cd    : '{comp_cd}'")
            print(f"branch_cd  : '{branch_cd}'")
            print(f"tran_cd    : {tran_cd}")
            print(f"tran_dt    : '{tran_dt}'")


            query = """
            SELECT *
            FROM daily_trn
            WHERE
                TRIM(comp_cd) = %s
                AND TRIM(branch_cd) = %s
                AND tran_cd = %s
                AND DATE(tran_dt) = %s::date
            LIMIT 1;
            """


            cursor.execute(
                query,
                (
                    comp_cd.strip(),
                    branch_cd.strip(),
                    tran_cd,
                    tran_dt
                )
            )


            transaction = cursor.fetchone()


            print("\nDatabase returned:")

            if transaction:
                print(transaction)

            else:
                print("No transaction found")


            return transaction


        except Exception as e:

            print(
                "Repository Error:",
                e
            )

            return None


        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()