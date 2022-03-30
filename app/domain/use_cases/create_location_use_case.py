from app.domain.use_cases import base_location_use_case
from app.domain import model


class CreateLocationUseCase(base_location_use_case.BaseLocationUseCase):

    def create(self, location: model.Location) -> int:
        return self.repository.create(location)
