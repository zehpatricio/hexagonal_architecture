from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship

from app.adapter.sql_alchemy import sql_db


class User(sql_db.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    devices = relationship("Device", back_populates="user")


class Device(sql_db.Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="devices")
    locations = relationship("Location", back_populates="device")


class Location(sql_db.Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    lat = Column(Float)
    long = Column(Float)
    date = Column(DateTime)

    device = relationship("Device", back_populates="locations")
