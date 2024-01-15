from database.schema import Logs
from typing import List

from utils.interface import CreateLog


# class Logs(Document):

#     staff_detected = ReferenceField(Staffs, required=False)

#     location = StringField(required=True)

#     time_of_detection = DateTimeField(required=True)

#     created_at = DateTimeField(default=datetime.now())

#     updated_at = DateTimeField(default=datetime.now())


class LogsRepository:
    @staticmethod
    async def pagination(page_number, per_page):
        offset = (page_number - 1) * per_page

        query: List[Logs] = (
            Logs.objects().order_by("-updated_at").skip(offset).limit(per_page)
        )

        recordings = [recording.to_dict() for recording in query]

        return recordings

    @staticmethod
    def create_log(log: CreateLog):
        query = Logs(
            staff_detected=log.staff_detected,
            location=log.location,
            time_of_detection=log.time_of_detection,
            is_unknown=log.is_unknown,
        )

        query.save()
