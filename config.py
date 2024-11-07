import os


SQLALCHEMY_DATABASE_URI = 'sqlite:///flashcards.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)  # Generates a random secret key for CSRF protection

