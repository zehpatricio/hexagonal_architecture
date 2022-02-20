import typing
import fastapi

from app.adapter import location_repository_impl
from app.domain.use_cases.location import list_location_use_case
from app.domain.use_cases.location import create_location_use_case
from app.domain import model

app = fastapi.FastAPI()

repository = location_repository_impl.LocationRepositoryImpl()
list_uc = list_location_use_case.ListLocationUseCase(repository)
create_uc = create_location_use_case.CreateLocationUseCase(repository)

@app.get('/locations/')
def list(user_id=None, device_id=None):
    return list_uc.list(user_id=user_id, device_id=device_id)


@app.post('/locations/')
def create(locations: typing.List[model.Location]):
    return create_uc.create(locations)
