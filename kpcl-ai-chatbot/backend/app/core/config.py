import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 🚀 THE FIX: Force Python to read the .env file BEFORE doing anything else
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "KPCL AI Chatbot"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 🔴 Now this will correctly grab the key!
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.5-flash") 
    
    # Ollama Local Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Data Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ACTIVE_DATA_PATH: str = os.path.join(BASE_DIR, "data", "raw", "Warranty Claims Cleaned MasterDataset.xlsx")
    KB_DATA_PATH: str = os.path.join(BASE_DIR, "data", "raw", "knowledge_base.xlsx")
    
    # 💰 NEW: Cost Analysis Path
    COST_DATA_PATH: str = os.path.join(BASE_DIR, "data", "raw", "cost_Analysis_for_spare_part_cc.xlsx")
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

settings = Settings()