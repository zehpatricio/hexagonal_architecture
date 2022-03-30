from datetime import datetime


class Location():
    id: int
    lat: float
    long: float
    date: datetime

    def __init__(
        self, id, lat, long, date
    ) -> None:
    
        self.id = id
        self.lat = lat
        self.long = long
        self.date = date
