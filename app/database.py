import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import Config
from app.logger import logger


class Database:
    """
    Handles PostgreSQL Connection
    """


    def __init__(self):

        self.connection = None



    def connect(self):

        try:

            if self.connection is None or self.connection.closed:

                self.connection = psycopg2.connect(

                    host=Config.DB_HOST,

                    port=Config.DB_PORT,

                    database=Config.DB_NAME,

                    user=Config.DB_USER,

                    password=Config.DB_PASSWORD,

                    cursor_factory=RealDictCursor

                )


                # Required for LISTEN / NOTIFY

                self.connection.set_isolation_level(

                    psycopg2.extensions
                    .ISOLATION_LEVEL_AUTOCOMMIT

                )


                logger.info(
                    "PostgreSQL connection established"
                )


            return self.connection



        except Exception as e:

            logger.exception(
                "Database connection failed"
            )

            raise e




    def cursor(self):

        if self.connection is None:

            self.connect()


        return self.connection.cursor()



    def close(self):

        if self.connection:


            self.connection.close()


            self.connection = None


            logger.info(
                "PostgreSQL connection closed"
            )