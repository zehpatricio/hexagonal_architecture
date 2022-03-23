from datetime import datetime


class Location():
    id: int
    device_id: int
    lat: float
    long: float
    date: datetime

    def __init__(
        self, id, device_id, lat, long, date
    ) -> None:
    
        self.id = id
        self.device_id = device_id
        self.lat = lat
        self.long = long
        self.date = date
