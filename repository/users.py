from authentication.hashing import hashPassword
from database.schema import Users
from validation.model import CreateUser
from utils.validate import get_object_id





class UsersRepository:
    @staticmethod
    async def create_user(user: CreateUser) -> Users:
        query = Users(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=hashPassword(user.password),
        )

        query.save()

        return query


    @staticmethod
    async def get_user_by_email(email:str) -> Users:

        query = Users.objects(email=email).first()
        return query

    

    @staticmethod
    async def get_user_by_id(user_id:str) -> Users:

        query = Users.objects(id=get_object_id(user_id)).first()
        
        return query
