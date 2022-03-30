import abc
from typing import List

from app.domain import model


class LocationRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def list(self) -> List[model.Location]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, location: model.Location) -> int:
        raise NotImplementedError
