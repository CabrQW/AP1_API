import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///reservas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title": "API de Reservas",
        "uiversion": 3
    }
