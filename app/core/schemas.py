from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field

SRID = 4326


class Geopoint(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)

    def to_wkt(self) -> WKTElement:
        return WKTElement(
            f"POINT({self.lon} {self.lat})",
            srid=SRID,
        )

    @classmethod
    def from_wkb(cls, value):
        if value is None:
            return None
        point = to_shape(value)
        return cls(lat=point.y, lon=point.x)
