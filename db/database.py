# db/database.py
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_base_dir():
    if getattr(sys, 'frozen', False):  # Detecta si es .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "data", "entrenamiento.db")  # Ruta final

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
