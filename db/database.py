# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Crear el motor SQLite (se guarda en archivo local)
engine = create_engine("sqlite:///data/entrenamientos.db", echo=False)

# Base declarativa para modelos
Base = declarative_base()

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
