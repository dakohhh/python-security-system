import typing
from database.schema import UniversityMember, SecurityPersonnel


class UniversityMemberRepository:

    @staticmethod
    def get_all_university_members() -> typing.List[UniversityMember]:
        query = UniversityMember.objects()

        return query
    

    @staticmethod
    async def get_security_personnels() -> typing.List[SecurityPersonnel]:

        query = UniversityMember.objects(is_security_personnel=True)

        return query
