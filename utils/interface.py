from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from database.schema import Students
from pydantic import BaseModel, validator
from exceptions.custom_exception import BadRequestException





class Token(BaseModel):
    user: str
    exp:int

    def get_expiry_time(self):
        return datetime.utcfromtimestamp(self.exp)




@dataclass_json
@dataclass
class StudentHaveData:
    student: Students
    status: bool

