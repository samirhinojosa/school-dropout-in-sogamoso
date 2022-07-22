from pydantic import BaseModel

class Student(BaseModel):
    id: int
    gender: str
    age: int
    institution: str
    schoolGrade: int
    schoolDay: str
    stratum: str
    disability: str
    countryOrigin: str
    shapPosition: int