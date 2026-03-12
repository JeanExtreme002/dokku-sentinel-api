import os

import dotenv

dotenv.load_dotenv()


class Config:
    """
    Base configuration.
    """

    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "5000"))
    API_WORKERS_COUNT = int(os.getenv("API_WORKERS_COUNT", "1"))
    API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"
    API_LOG_LEVEL = os.getenv("API_LOG_LEVEL", "INFO").lower()

    MASTER_KEY: str = os.getenv("MASTER_KEY")
