from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
# from database.schema import Students
from pydantic import BaseModel, validator
from database.schema import Staffs
from exceptions.custom_exception import BadRequestException





class Token(BaseModel):
    user: str
    exp:int

    def get_expiry_time(self):
        return datetime.utcfromtimestamp(self.exp)




@dataclass
class CreateLog:

    staff_detected : Staffs 
    location: str
    is_unknown: bool
    time_of_detection: datetime




    pass


@dataclass_json
@dataclass
class StudentHaveData:
    student: None
    status: bool




if __name__ == "__main__":


    print("wisdom")
