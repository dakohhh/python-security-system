from datetime import datetime
from mongoengine import Document, StringField, IntField, BooleanField, EmailField, DateTimeField



class Users(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    email = EmailField(required=True, unique=True)

    password = StringField(required=True)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"collection": "users", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email, 
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }




class Students(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    matric_no = IntField(required=True, unique=True)

    is_blacklisted = BooleanField(required=True, default=False)

    has_data = BooleanField(required=True, default=False)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())


    meta = {"collection": "students"}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "matric_no": self.matric_no,
            "is_blacklisted": self.is_blacklisted,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    





class Recordings(Document):

    name = StringField(required=True, max_length=50)

    url = StringField(required=True)

    time_of_detection = DateTimeField(required=True)

    is_detected_blacklist = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())



    meta = {"collection": "recordings", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "name": self.name,
            "url": self.url,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }




















