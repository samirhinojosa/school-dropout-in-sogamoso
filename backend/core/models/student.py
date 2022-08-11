from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Float
)

# from settings.database import Base
from .base_model import Base

class Student(Base):
    __tablename__ = "students"

    idx = Column(Integer, primary_key=True, index=True)
    anyo = Column(Integer)
    institucion = Column(String)
    per_id_anyo = Column(Integer)
    per_id = Column(Integer)
    edad = Column(Integer)
    edad_clasificacion = Column(String)
    genero = Column(String)
    grado_cod = Column(Float)
    jornada = Column(String)
    estado = Column(Integer)
    estrato = Column(String)
    pais_origen = Column(String)
    discapacidad = Column(String)
    srpa = Column(String)
    institucion_sector = Column(String)
    institucion_modelo = Column(String)
    institucion_apoyo_academico_especial = Column(String)
    institucion_zona = Column(String)
    institucion_caracter = Column(String)
    institucion_numero_de_sedes = Column(Float)
    institucion_estado = Column(String)
    institucion_latitude = Column(String)
    institucion_longitud = Column(String)
    institucion_prestador_de_servicio = Column(String)
    institucion_tamanyo = Column(String)
    institucion_nivel_basica_primaria = Column(Integer)
    institucion_nivel_secundaria_primaria = Column(Integer)
    institucion_nivel_media = Column(Integer)
    institucion_nivel_preescolar = Column(Integer)
    institucion_nivel_primera_infancia = Column(Integer)
    institucion_especialidad_academica = Column(Integer)
    institucion_especialidad_agropecuario = Column(Integer)
    institucion_especialidad_comercial = Column(Integer)
    institucion_especialidad_industrial = Column(Integer)
    institucion_especialidad_no_aplica = Column(Integer)
    institucion_especialidad_otro = Column(Integer)