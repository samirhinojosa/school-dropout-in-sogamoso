from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Students(Base):
    __tablename__ = "students_table"

    index = Column(Integer, primary_key=True, index=True)
    ANO = Column(Integer)
    INSTITUCION = Column(String)
    PER_ID_ANO = Column(Integer)
    PER_ID = Column(Integer)
    EDAD = Column(Integer)
    GENERO = Column(String)
    GRADO_COD = Column(Float)
    JORNADA = Column(String)
    ESTADO = Column(Integer)
    ESTRATO = Column(String)
    PAIS_ORIGEN = Column(String)
    DISCAPACIDAD = Column(String)
    SRPA = Column(String)
    INSTITUCION_SECTOR = Column(String)
    INSTITUCION_MODELO = Column(String)
    INSTITUCION_APOYO_ACADEMICO_ESPECIAL = Column(String)
    INSTITUCION_ZONA = Column(String)
    INSTITUCION_CARACTER = Column(String)
    INSTITUCION_NUMERO_DE_SEDES = Column(Float)
    INSTITUCION_ESTADO = Column(String)
    INSTITUCION_LATITUDE = Column(Float)
    INSTITUCION_LONGITUD = Column(Float)
    INSTITUCION_PRESTADOR_DE_SERVICIO = Column(String)
    INSTITUCION_TAMAÑO = Column(String)
    INSTITUCION_NIVEL_BASICA_PRIMARIA = Column(Integer)
    INSTITUCION_NIVEL_SECUNDARIA_PRIMARIA = Column(Integer)
    INSTITUCION_NIVEL_MEDIA = Column(Integer)
    INSTITUCION_NIVEL_PREESCOLAR = Column(Integer)
    INSTITUCION_NIVEL_PRIMERA_INFANCIA = Column(Integer)
    INSTITUCION_ESPECIALIDAD_ACADÉMICA = Column(Integer)
    INSTITUCION_ESPECIALIDAD_AGROPECUARIO = Column(Integer)
    INSTITUCION_ESPECIALIDAD_COMERCIAL = Column(Integer)
    INSTITUCION_ESPECIALIDAD_INDUSTRIAL = Column(Integer)
    INSTITUCION_ESPECIALIDAD_NO_APLICA = Column(Integer)
    INSTITUCION_ESPECIALIDAD_OTRO = Column(Integer)

