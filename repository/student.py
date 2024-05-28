import typing

from beanie import PydanticObjectId
from database.schema import Student
from validation.model import CreateStudent


class StudentRepository:
    @staticmethod
    async def does_matric_no_exists(matric_no: str):
        query = Student.objects(matric_no=matric_no).first()

        return query is not None
    
    @staticmethod
    async def does_student_exists(student_id: PydanticObjectId):
        query = Student.objects(id=student_id).first()

        return query is not None

    @staticmethod
    async def create_student(student: CreateStudent) -> Student:
        new_student = Student(
            firstname=student.firstname,
            lastname=student.lastname,
            matric_no=student.matric_no,
        )

        new_student.save()

        return new_student

    @staticmethod
    async def get_all_student() -> typing.List[Student]:
        query = Student.objects()

        return query

    @staticmethod
    async def get_all_students_without_encodings() -> typing.List[Student]:
        pipeline = [
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "firstname": 1,
                    "lastname": 1,
                    "has_data":1,
                    "matric_no": 1,
                    "created_at": 1,
                    "updated_at": 1,
                }
            }
        ]

        query = Student.objects.aggregate(*pipeline)

        return query

    
    

    @staticmethod
    async def delete_student(student_id: PydanticObjectId):
        Student.objects(id=student_id).delete()
