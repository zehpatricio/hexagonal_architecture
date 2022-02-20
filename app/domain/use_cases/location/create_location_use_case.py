from typing import List


from app.domain.use_cases.location import base_location_use_case
from app.domain import model

class CreateLocationUseCase(base_location_use_case.BaseLocationUseCase):

    def create(self, locations: List[model.Location]) -> List[int]:
        return self.repository.create(locations)
