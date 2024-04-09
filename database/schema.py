from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    EmailField,
    DateTimeField,
    ReferenceField,
    ListField,
)


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
            "id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class UniversityMember(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    has_data = BooleanField(required=True, default=False)

    encodings = ListField(required=False, default=[])

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"collection": "university_member", "strict": False, "allow_inheritance": True}

    def to_dict(self):

        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class Student(UniversityMember):

    matric_no = IntField(required=True)

    def to_dict(self) -> dict:

        klass = super().to_dict()

        klass.update({"matric_no": self.matric_no})

        return klass


class SecurityPersonnel(UniversityMember):

    staff_id = IntField(required=True)

    phone_number = StringField(required=True)

    is_security_personnel = BooleanField(required=True, default=True)

    meta = {"strict": False}

    def to_dict(self) -> dict:

        klass = super().to_dict()

        klass.update(
            {
                "staff_id": self.staff_id,
                "phone_number": self.phone_number,
                "is_security_personnel": self.is_security_personnel,
            }
        )

        return klass


class Logs(Document):

    student_detected: Student = ReferenceField(Student, required=False, default=None)

    location = StringField(required=True)

    time_of_detection = DateTimeField(required=True)

    is_unknown = BooleanField(required=True, default=False)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"collection": "logs", "strict": False}

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "staff_detected": (
                self.student_detected.to_dict()
                if self.student_detected
                else self.student_detected
            ),
            "location": self.location,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
