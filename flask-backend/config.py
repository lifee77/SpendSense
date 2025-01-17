import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SUPABASE_URL', 'your_supabase_uri_here')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', 'your_api_key_here')
