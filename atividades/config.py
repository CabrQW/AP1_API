import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///atividades.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title": "API de Atividades e Notas",
        "uiversion": 3
    }
