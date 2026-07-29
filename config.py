import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY',"ml_preprocessing_studio_2026")