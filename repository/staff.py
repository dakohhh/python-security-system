import typing
from database.schema import Staffs
from utils.interface import StudentHaveData
from utils.validate import get_object_id
from validation.model import CreateStaff


class StaffRepository:
    @staticmethod
    async def does_staff_id_exist(staff_id: str):
        query = Staffs.objects(staff_id=staff_id).first()

        return query is not None

    @staticmethod
    async def create_staff(staff: CreateStaff) -> Staffs:
        new_staff = Staffs(
            firstname=staff.firstname,
            lastname=staff.lastname,
            phone_number=staff.phone_number,
            is_security_personnel=staff.is_security_personnel,
            staff_id=staff.staff_id,
        )

        new_staff.save()

        return new_staff

    @staticmethod
    def get_all_staffs() -> typing.List[Staffs]:
        query = Staffs.objects()

        return query
    

    @staticmethod
    async def get_security_personnel_staffs() -> typing.List[Staffs]:

        query = Staffs.objects(is_security_personnel=True)

        return query
