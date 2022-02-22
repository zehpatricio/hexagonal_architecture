import typing
import dataset

from app.common import exception
from app.domain.repository import location_repository
from app.domain import model


class LocationRepositoryImpl(location_repository.LocationRepository):

    def __init__(self) -> None:
        self.db = dataset.connect('sqlite:///database.db')
        self.table_location = self.db.create_table('location')
        self.table_user = self.db.create_table('user')
        self.table_device = self.db.create_table('device')

    def list(
        self, user_id=None, device_id=None
    ) -> typing.List[model.Location]:

        if device_id:
            found_locations = self.table_location.find(device_id=device_id)
        elif user_id:
            found_devices = self.table_device.find(user_id=user_id)
            devices_ids = ', '.join([str(d['id']) for d in found_devices])
            stmt = f'SELECT * FROM location WHERE device_id IN ({devices_ids})'

            found_locations = self.db.query(stmt) if devices_ids else []
        else:
            found_locations = self.table_location.all()

        locations = [model.Location(**l) for l in found_locations]

        return locations

    def create(
        self, locations: typing.List[model.Location]
    ) -> typing.List[int]:

        dict_locations = [l.dict() for l in locations]
        locations_devices_ids = {d['device_id'] for d in dict_locations}
        existent_devices_ids = set([d['id'] for d in self.table_device.all()])
        not_existent_ids = locations_devices_ids - existent_devices_ids

        if not_existent_ids:
            raise exception.DeviceNotFoundException()

        return self.table_location.insert_many(dict_locations)
