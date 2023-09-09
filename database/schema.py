from datatime import datetime
from mongoengine import Document, StringField, IntField, BooleanField, EmailField, DateTimeField



class Users(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    email = EmailField()

    password = StringField(required=True)

    created_at = DateTimeField(default=datetime.now())
    
    updated_at = DateTimeField(default=datetime.now())

    meta = {"collection": "users", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }




class Students(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    matric_no = IntField(required=True, unique=True)

    is_blacklisted = BooleanField(required=True, default=False)


    meta = {"collection": "students", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "matric_no": self.matric_no,
            "is_blacklisted": self.is_blacklisted
        }
    





class Students(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    matric_no = IntField(required=True, unique=True)

    d = BooleanField(required=True, default=False)


    meta = {"collection": "students", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "matric_no": self.matric_no,
            "is_blacklisted": self.is_blacklisted
        }




















