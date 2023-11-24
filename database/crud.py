from typing import List, Type, Union
from mongoengine import Document
from mongoengine.errors import MongoEngineException
from .schema import Users, Students
from exceptions.custom_exception import ServerErrorException, BadRequestException





async def fetchone_document(klass:Type[Document], *args, **kwargs)-> Union[Users, Students, None]:
    try:
        return klass.objects.get(*args, **kwargs)
    
    except klass.DoesNotExist:
        return None
    
    except Exception as e:
        raise ServerErrorException(str(e))
    


async def fetchall_documents(klass:Type[Document], *args, **kwargs)-> List[Users]:

    try:
        return klass.objects(*args, **kwargs)
    
    except klass.DoesNotExist:
        return klass.objects(*args, **kwargs)
    
    except Exception as e:
        raise ServerErrorException(str(e))



async def fetchall(klass:Type[Document]) ->Union[List[Users], None]:
    try:
        return klass.objects().all()
     
    except Exception as e:
        raise ServerErrorException(str(e))



  




