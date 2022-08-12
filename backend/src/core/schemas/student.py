from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
    MALE = "FEMENINO"
    FEMALE = "MASCULINO"


class SchoolDay(str, Enum):
    MORNING = "MAÑANA"
    AFTERNOON = "TARDE"
    NOCTURNAL = "NOCTURNA"
    UNIQUE = "ÚNICA"
    COMPLETE = "COMPLETA"
    WEEKEND = "FIN DE SEMANA"


class Stratum(str, Enum):
    STRATUM_0 = "ESTRATO 0"
    STRATUM_1 = "ESTRATO 1"
    STRATUM_2 = "ESTRATO 2"
    STRATUM_3 = "ESTRATO 3"
    STRATUM_4 = "ESTRATO 4"
    STRATUM_5 = "ESTRATO 5"
    STRATUM_6 = "ESTRATO 6"


class StudentId(BaseModel):
    ids: list[int] = []

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    id: int

class Student(StudentBase):
    gender: Gender
    age: int
    institution: str
    schoolGrade: int
    schoolDay: SchoolDay
    stratum: Stratum
    disability: str
    countryOrigin: str
    shapPosition: int

    class Config:
        orm_mode = True


# class StudentBase(BaseModel):
#     ids: int


# class StudentId(BaseModel):
#     ids: list[StudentBase] = []

#     class Config:
#         orm_mode = True


# class Student(StudentBase):
#     gender: Gender
#     age: int
#     institution: str
#     schoolGrade: int
#     schoolDay: SchoolDay
#     stratum: Stratum
#     disability: str
#     countryOrigin: str
#     shapPosition: int

#     class Config:
#         orm_mode = True