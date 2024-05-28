from database.schema import Staff
from validation.model import CreateStaff



class StaffRepository():

    @staticmethod
    async def create_staff(staff:CreateStaff):
        new_staff = Staff(
            firstname=staff.firstname,
            lastname=staff.lastname,
            staff_id=staff.staff_id,
            phone_number=staff.phone_number
        )

        new_staff.save()

        return new_staff