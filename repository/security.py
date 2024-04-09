import typing
from database.schema import SecurityPersonnel
from utils.interface import StudentHaveData
from utils.validate import get_object_id
from validation.model import CreateSecurityPersonnel



class SecurityPersonnelRepository:
    @staticmethod
    async def does_staff_id_exists(staff_id: str):
        query = SecurityPersonnel.objects(staff_id=staff_id).first()

        return query is not None

    @staticmethod
    async def create_security_personnel(security_personnel: CreateSecurityPersonnel) -> SecurityPersonnel:
        new_security_personnel = SecurityPersonnel(
            firstname=security_personnel.firstname,
            lastname=security_personnel.lastname,
            staff_id=security_personnel.staff_id,
            phone_number=security_personnel.phone_number
        )

        new_security_personnel.save()

        return new_security_personnel

    @staticmethod
    def get_all_security_personnel() -> typing.List[SecurityPersonnel]:
        query = SecurityPersonnel.objects()

        return query

    @staticmethod
    async def get_security_personnel() -> typing.List[SecurityPersonnel]:

        query = SecurityPersonnel.objects(is_security_personnel=True)

        return query
