from database.schema import Students





class StudentsRepository:

    @staticmethod
    async def does_matric_exist(matric_no:int):

        student = Students.objects.get(matric_no=matric_no)
        
        return student is not None
    
    @staticmethod
    async def change_student_data_status(student:Students):

        student.has_data = True

        student.save()

