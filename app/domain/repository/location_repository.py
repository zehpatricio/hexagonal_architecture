import abc
from typing import List

from app.domain import model


class LocationRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def list(self, device_id=None) -> List[model.Location]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, locations: List[model.Location]) -> List[int]:
        raise NotImplementedError
