import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "KPCL AI Chatbot"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Ollama Local Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "qwen2.5-coder:7b") 
    
    # Data Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 🔴 UPDATE THIS LINE to point to your new file:
    ACTIVE_DATA_PATH: str = os.path.join(BASE_DIR, "data", "raw", "Warranty Claims Cleaned MasterDataset.xlsx")
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

settings = Settings()