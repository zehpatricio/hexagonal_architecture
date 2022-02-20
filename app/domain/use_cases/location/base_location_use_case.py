from app.domain.repository import location_repository


class BaseLocationUseCase():

    def __init__(
        self,
        repository: location_repository.LocationRepository
    ) -> None:
        self.repository = repository
