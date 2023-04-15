from os import getenv

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
DB_URI = getenv("DB_URI")
PORT = int(getenv("PORT", "8000"))
HOST = getenv("HOST", "0.0.0.0")
