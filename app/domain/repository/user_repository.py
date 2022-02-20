import abc

from model import User


class UserRepository():

    @abc.abstractmethod
    def create(self, user: User) -> int:
        raise NotImplementedError
