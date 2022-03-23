from app.domain import model as domain_model
from app.adapter.rest import model as rest_model


def to_domain_model(location: rest_model.Location) -> domain_model.Location:
    domain_location = domain_model.Location(**vars(location))

    return domain_location


def to_rest_model(location: domain_model.Location) -> rest_model.Location:
    rest_location = rest_model.Location(**vars(location))

    return rest_location
