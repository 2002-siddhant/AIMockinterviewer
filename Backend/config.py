import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")