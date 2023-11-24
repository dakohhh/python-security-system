from authentication.hashing import hashPassword
from database.schema import Users
from validation.model import CreateUser






class UsersRepository:
    @staticmethod
    async def create_user(user: CreateUser) -> Users:
        new_user = Users(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=hashPassword(user.password),
        )

        new_user.save()

        return new_user
