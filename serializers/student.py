from pydantic import BaseModel
from beanie import PydanticObjectId
import json
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from.university_member import UniversityMemberSerializer


class StudentSerializer(UniversityMemberSerializer):
    matric_no: int


class AllStudentSerializer(BaseModel):
    students: List[StudentSerializer]

    @property
    def model_serialize(self):
        return json.loads(super().model_dump_json())
