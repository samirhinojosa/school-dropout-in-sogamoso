from typing import Optional
from fastapi import Depends, HTTPException
import src.core.schemas.student as schestu
from src.core.repositories.student import StudentRepository


class StudentService:


    def __init__(self, student_repository: StudentRepository = Depends()) -> None:
        self.student_repository = student_repository


    def get_students_id(self, skip: Optional[int] = 0, limit: Optional[int] = 1000) -> dict:
        """ 
        Fetch all students id

        Parameters:
            skip (int): Pagination starting.
            limit (int): End of pagination.
            
        Returns:
            ids (dict) : List of students id.
        """ 

        return {
            "ids" : self.student_repository.get_students_id(skip=skip, limit=limit)
        }  

    
    def get_student_summary_by_id(self, id: int) -> dict:
        """ 
        Fetch a summary student based on id

        Parameters:
            id (int): Student id.
            
        Returns:
            student (dict) : Summary student.
        """ 

        result = self.student_repository.get_student_summary_by_id(id)

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        else:
            student = {
                "id" : result[0],
                "gender" : result[1],
                "age" : result[2],
                "institution" : result[3],
                "schoolGrade" : result[4],
                "schoolDay" : result[5],
                "stratum" : result[6],
                "disability" : result[7],
                "countryOrigin" : result[8],
                "shapPosition" : result[9]
            }

            return student

    
    def get_statistics_age(self) -> list:
        """ 
        Fetch student statistics by age

        Returns:
            (dict) : Student age statistics.
        """ 

        result = self.student_repository.get_statistics_age()

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student age statistis not found")
        else:
            return {"ages_not_dropout" : result[0], "ages_dropout" : result[1]}


    def get_statistics_stratum(self) -> list:
        """ 
        Fetch student statistics by stratum

        Returns:
            (dict) : Student stratum statistics.
        """ 

        result = self.student_repository.get_statistics_stratum()

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student stratum statistis not found")
        else:
            return {"stratums_not_dropout" : result[0], "stratums_dropout" : result[1]}
