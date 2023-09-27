import datetime
from pydantic import BaseModel, validator
from exceptions.custom_exception import BadRequestException




class Token(BaseModel):
    user: str
    exp:str

    @validator("exp")
    def parse_exp(cls, exp):
        try:

            timestamp_datetime = datetime.datetime.utcfromtimestamp(int(exp))

            return timestamp_datetime
        
        except ValueError:

            raise BadRequestException(f"invalid date format for 'exp', got {exp}, expected '16xxxxxxxx'")

