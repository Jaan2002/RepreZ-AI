from dotenv import load_dotenv
import os
load_dotenv()
APP_NAME = os.getenv("APP_NAME","Reprez")
APP_VERSION= os.getenv("APP_VERSION","0.1.0")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")