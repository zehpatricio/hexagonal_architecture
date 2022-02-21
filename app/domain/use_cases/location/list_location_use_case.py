from typing import List

from app.domain.model import Location
from app.domain.use_cases.location import base_location_use_case


class ListLocationUseCase(base_location_use_case.BaseLocationUseCase):

    def list(self, user_id=None, device_id=None) -> List[Location]:
        locations = self.repository.list(user_id=user_id, device_id=device_id)
        locations.sort(key=lambda l: l.date)

        return locations
