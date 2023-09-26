from database.schema import Recordings







class RecordingsRepository():

    @staticmethod
    async def pagination(page_number, per_page):

        offset = (page_number - 1) * per_page

        recordings = Recordings.objects().order_by('-updated_at').skip(offset).limit(per_page)

        return recordings


    @staticmethod
    async def get_total_recordings():

        total_orders = Recordings.objects().count()

        return total_orders
