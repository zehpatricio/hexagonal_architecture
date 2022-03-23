from sqlalchemy import Column, Integer, Float, DateTime

from app.adapter.db import sql_db


class Location(sql_db.Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    lat = Column(Float)
    long = Column(Float)
    date = Column(DateTime)
