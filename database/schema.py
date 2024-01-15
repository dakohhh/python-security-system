from datetime import datetime
from mongoengine import Document, StringField, IntField, BooleanField, EmailField, DateTimeField, ReferenceField, ListField



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



class Staffs(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    staff_id = StringField(required=True, default="1234")

    has_data = BooleanField(required=True, default=False)

    encodings = ListField(required=False, default=[])

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())


    meta = {"collection": "staffs"}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "staff_id": self.staff_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    



class SecurityPersonels(Document):
    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    phone_number = IntField(required=True)

    pass

class Logs(Document):

    staff_detected = ReferenceField(Staffs, required=False, default=None)

    location = StringField(required=True)

    time_of_detection = DateTimeField(required=True)

    is_unknown = BooleanField(required=True, default=False)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())



    meta = {"collection": "logs", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "name": self.name,
            "location": self.location,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }




















