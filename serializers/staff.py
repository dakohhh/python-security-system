from .university_member import UniversityMemberSerializer
from pydantic import BaseModel
from typing import List


class UniversityStaff(UniversityMemberSerializer):
    staff_id: int
    is_security_personnel: bool
    phone_number: str



class AllUniversityStaffSerializer(BaseModel):
    
    staffs: List[UniversityStaff]