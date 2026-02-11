import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'news_analyzer'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    SCRAPE_INTERVAL_HOURS = int(os.getenv('SCRAPE_INTERVAL_HOURS', 1))
    MAX_ARTICLES_PER_SOURCE = int(os.getenv('MAX_ARTICLES_PER_SOURCE', 50))
    
    MALAYSIAN_STATES = [
        'Johor', 'Kedah', 'Kelantan', 'Melaka', 'Negeri Sembilan',
        'Pahang', 'Penang', 'Perak', 'Perlis', 'Sabah', 'Sarawak',
        'Selangor', 'Terengganu', 'Kuala Lumpur', 'Putrajaya', 'Labuan'
    ]
    
    @staticmethod
    def get_db_connection_string():
        """Get database connection string for logging"""
        db = Config.DB_CONFIG
        return f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['database']}"

db_config = Config.DB_CONFIG