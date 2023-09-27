import os
import jwt
import datetime
from dotenv import load_dotenv
from utils.interface import Token
from exceptions.custom_exception import CredentialsException

load_dotenv()




def create_access_token(data):
    token = jwt.encode({
        "user":data, 

        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)

        }, str(os.getenv("SECRET_KEY"))    
    )
    
    return token





def verify_access_token(token:str):
    try:

        payload_instance = jwt.decode(token, str(os.getenv("SECRET_KEY")), algorithms=["HS256"])

        payload = Token.parse_obj(payload_instance)

        if payload.exp < datetime.datetime.utcnow():

            raise CredentialsException("token has expired")
        
        return payload
    
    except jwt.PyJWTError as e:
        raise CredentialsException(str(e))
    




