from abc import ABC, abstractmethod

from domain.models.urls import Urls


class AbstractUrlService(ABC):

    @abstractmethod
    def get_urls(self) -> Urls: raise NotImplementedError
