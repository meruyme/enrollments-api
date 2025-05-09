from app.core.settings import Settings

from app.utils.external_requests import external_get_request

settings = Settings()


class AgeGroupApiClient:

    @staticmethod
    def get_age_groups_by_age(age: int) -> list:
        return external_get_request(
            url=settings.age_group_api_base_url,
            params={"age": age},
            username=settings.age_group_api_username,
            password=settings.age_group_api_password
        )
