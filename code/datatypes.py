from dataclasses import dataclass
from enum import StrEnum
from os import PathLike


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class Icon:
    filename: PathLike | str

    def __post_init__(self):
        # make it str for folium compatibility (can use only `str` for icon path)
        if not isinstance(self.filename, str):
            self.filename = str(self.filename)


class MapObjectType(StrEnum):
    LOREBOOK = 'Lorebook'
    TREASURE = 'Treasure'
    SKYSHARD = 'Skyshard'


@dataclass
class MapObject:
    type: MapObjectType
    coordinate: Coordinate
    icon: Icon
    name: str = ''


@dataclass(kw_only=True)
class Lorebook(MapObject):
    type: MapObjectType = MapObjectType.LOREBOOK
    some_number_1: int
    some_number_2: int
