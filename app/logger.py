import logging
import os

from app.config import Config

os.makedirs("logs", exist_ok=True)

logging.basicConfig(

    level=getattr(logging, Config.LOG_LEVEL),

    format="%(asctime)s | %(levelname)s | %(message)s",

    handlers=[

        logging.FileHandler("logs/fraud_detection.log"),

        logging.StreamHandler()

    ]
)

logger = logging.getLogger("FraudDetection")