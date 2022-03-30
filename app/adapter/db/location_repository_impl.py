import typing

from app.domain.repository import location_repository
from app.domain import model as domain_model
from app.adapter.db import sql_db
from app.adapter.db import model as sql_model
from app.adapter.db import location_mapper


class LocationRepositoryImpl(location_repository.LocationRepository):

    def __init__(self) -> None:
        self.db = sql_db.get_db()

    def list(self) -> typing.List[domain_model.Location]:
        found_locations = self.db.query(sql_model.Location).all()
        locations = map(location_mapper.to_domain_model, found_locations)

        return locations

    def create(
        self, location: domain_model.Location
    ) -> int:

        db_location = location_mapper.to_sql_model(location)
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)

        return db_location.id
