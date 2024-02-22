from database.schema import Logs
from typing import List

from utils.interface import CreateLog



class LogsRepository:
    @staticmethod
    async def get_all_logs(page_number, per_page) -> List[Logs]:
        offset = (page_number - 1) * per_page

        query: List[Logs] = (
            Logs.objects().order_by("-created_at").skip(offset).limit(per_page)
        )

        return query
        

    @staticmethod
    def create_log(log: CreateLog):
        query = Logs(
            staff_detected=log.staff_detected,
            location=log.location,
            time_of_detection=log.time_of_detection,
            is_unknown=log.is_unknown,
        )

        query.save()
