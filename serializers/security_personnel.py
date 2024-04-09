from pydantic import BaseModel
from beanie import PydanticObjectId
import json
from typing import List
from datetime import datetime
from bson import ObjectId


class SecurityPersonnelSerializer(BaseModel):
    id: PydanticObjectId
    firstname: str
    lastname: str
    staff_id: int
    phone_number:str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), ObjectId: lambda v: str(v)}


class AllSecurityPersonnelSerializer(BaseModel):
    security_personnels: List[SecurityPersonnelSerializer]

    @property
    def model_serialize(self):
        return json.loads(super().model_dump_json())
