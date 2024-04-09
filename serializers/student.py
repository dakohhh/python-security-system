from pydantic import BaseModel
from beanie import PydanticObjectId
import json
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class StudentSerializer(BaseModel):
    id: PydanticObjectId
    firstname: str
    lastname: str
    matric_no: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), ObjectId: lambda v: str(v)}


class AllStudentSerializer(BaseModel):
    students: List[StudentSerializer]

    @property
    def model_serialize(self):
        return json.loads(super().model_dump_json())
