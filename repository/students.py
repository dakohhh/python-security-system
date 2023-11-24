from database.schema import Students
from utils.interface import StudentHaveData
from validation.model import CreateStudent




class StudentsRepository:

    @staticmethod
    async def does_matric_exist(matric_no:int):

        student = Students.objects.get(matric_no=matric_no)
        
        return student is not None
    
    @staticmethod
    async def change_student_data_status(student:Students):

        student.has_data = True

        student.save()

    @staticmethod
    async def does_students_have_data() -> StudentHaveData:

        student = Students.objects.get(has_data=True)

        return StudentHaveData(student, student is not None)

    
    @staticmethod
    async def create_student(student: CreateStudent) -> Students:

        new_student = Students(**student)

        new_student.save()

        return new_student















