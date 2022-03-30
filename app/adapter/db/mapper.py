from app.domain import model as domain_model
from app.adapter.db import model as sql_model


def to_domain_model(location: sql_model.Location) -> domain_model.Location:
    domain_location = domain_model.Location(**vars(location))

    return domain_location


def to_sql_model(location: domain_model.Location) -> sql_model.Location:
    sql_location = sql_model.Location(**vars(location))

    return sql_location
