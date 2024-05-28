import typing

from beanie import PydanticObjectId
from database.schema import UniversityMember, SecurityPersonnel, UniversityStaff


class UniversityMemberRepository:

    @staticmethod
    def get_all_university_members() -> typing.List[UniversityMember]:
        query = UniversityMember.objects()

        return query
    

    @staticmethod
    async def get_security_personnels() -> typing.List[SecurityPersonnel]:

        query = UniversityMember.objects(is_security_personnel=True)

        return query
    
    
    @staticmethod
    async def does_staff_id_exists(staff_id: str):
        query = UniversityStaff.objects(staff_id=staff_id).first()

        return query is not None

    @staticmethod
    async def does_staff_exists(staff_id: PydanticObjectId):
        query = UniversityStaff.objects(id=staff_id).first()

        return query is not None
        
    @staticmethod
    async def all_university_staffs() -> typing.List[UniversityStaff]:
        pipeline = [
            {
                "$project": {
                    "id": { "$toString": "$_id" },
                    "firstname": 1,
                    "lastname": 1,
                    "matric_no": 1,
                    "has_data": 1,
                    "staff_id": 1,
                    "phone_number": 1,
                    "is_security_personnel": 1,
                    "created_at": 1,
                    "updated_at": 1,
                }
            }
        ]

        query = UniversityStaff.objects.aggregate(*pipeline)

        return query
    

    @staticmethod
    async def delete_staff(staff_id:PydanticObjectId):

        query = UniversityStaff.objects(id=staff_id)

        query.delete()

        return query
