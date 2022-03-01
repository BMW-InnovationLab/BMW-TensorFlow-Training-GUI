import json

from domain.models.urls import Urls
from domain.services.contract.abstract_url_service import AbstractUrlService


class UrlService(AbstractUrlService):
    def __init__(self):
        with open("./assets/environment.json", 'r') as urls_file:
            json_url = json.load(urls_file)
            self.urls: Urls = Urls.parse_obj(json_url)

    def get_urls(self) -> Urls:
        return self.urls
