from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from db.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    nombre_usuario = Column(String, unique=True, nullable=False)
    contrasena = Column(String)
    genero = Column(String)
    categoria = Column(String)
    nivel = Column(String)
    frecuencia_semanal = Column(Integer)


    planes = relationship("PlanEntrenamiento", back_populates="usuario")
    entrenamientos = relationship("Entrenamiento", back_populates="usuario")

class PlanEntrenamiento(Base):
    __tablename__ = 'planes_entrenamiento'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    semana = Column(Integer)
    dia = Column(String)
    disciplina = Column(String)
    descripcion = Column(String)
    duracion_min = Column(Integer)
    distancia_km = Column(Float)
    fecha = Column(Date)

    usuario = relationship("Usuario", back_populates="planes")

class Entrenamiento(Base):
    __tablename__ = 'entrenamientos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha = Column(Date)
    disciplina = Column(String)
    duracion = Column(Time)
    distancia_km = Column(Float)
    notas = Column(String)

    usuario = relationship("Usuario", back_populates="entrenamientos")
