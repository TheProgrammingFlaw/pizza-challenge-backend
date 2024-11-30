import os

class Config:
    FIREBASE_CREDENTIALS = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../serviceAccountKey.json')
