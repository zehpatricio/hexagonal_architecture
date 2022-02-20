import typing
from datetime import datetime

from app.domain.repository import location_repository
from app.domain import model


class LocationRepositoryImpl(location_repository.LocationRepository):

    locations = [model.Location(
        device_id = 1,
        lat = 2,
        long = 2,
        date = datetime.now(),
    )]

    def list(self, user_id=None, device_id=None) -> typing.List[model.Location]:
        return self.locations

    def create(
        self, locations: typing.List[model.Location]
    ) -> typing.List[int]:

        self.locations.extend(locations)
        return [1, 2, 3]
