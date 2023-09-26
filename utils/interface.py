from dataclasses import dataclass
from pydantic import BaseModel
from dataclasses_json import dataclass_json




@dataclass_json
@dataclass
class Token(BaseModel):
    user: str
    exp:str