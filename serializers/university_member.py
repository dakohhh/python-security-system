from pydantic import BaseModel






class UniversityMemberSerializer(BaseModel):
    id: str
    firstname: str
    lastname:str
    has_data: bool

    
