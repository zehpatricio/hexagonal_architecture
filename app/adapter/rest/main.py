import typing
import fastapi


from app.adapter.db import location_repository_impl
from app.domain.use_cases.location import list_location_use_case
from app.domain.use_cases.location import create_location_use_case
from app.adapter.rest import model
from app.adapter.rest import mapper

app = fastapi.FastAPI()

repository = location_repository_impl.LocationRepositoryImpl()
list_uc = list_location_use_case.ListLocationUseCase(repository)
create_uc = create_location_use_case.CreateLocationUseCase(repository)


@app.get('/locations/')
def list(device_id=None):
    return list_uc.list(device_id)


@app.post('/locations/')
def create(locations: typing.List[model.Location]):
    locations_domain = [mapper.to_domain_model(l) for l in locations]
    return create_uc.create(locations_domain)
