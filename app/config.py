import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 
    'postgresql://admin:adminpass@database/citas_medicas')
    SQLALCHEMY_TRACK_MODIFICATIONS = False