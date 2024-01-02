from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional, Literal

from app.html_map import Coordinates
from game_map.datatypes import GameIcon


class ObjectType(StrEnum):
    DEFENSIVE_SCROLL = auto()
    OFFENSIVE_SCROLL = auto()
    KEEP = auto()
    OUTPOST = auto()
    TOWN = 'avatown'
    GATE = 'borderkeep'
    TEMPLE = auto()


@dataclass
class Faction:
    full_name: str
    color: Literal['red', 'yellow', 'blue']

    @staticmethod
    def get_faction_by_keep_name(keep_name: str) -> 'Faction':
        if 'fort' in keep_name.lower():
            return COVENANT
        if 'keep' in keep_name.lower():
            return PACT
        if 'castle' in keep_name.lower():
            return DOMINION

        raise Exception(f'Wrong keep name `{keep_name}`')


COVENANT = Faction('Daggerfall Covenant', 'blue')
PACT = Faction('Ebonheart Pact', 'red')
DOMINION = Faction('Aldmeri Dominion', 'yellow')
NEUTRAL = Faction('Neutral', 'white')


@dataclass
class Object:
    type: ObjectType
    name: str
    coordinates: Coordinates
    icon: GameIcon = None
    faction: Optional[Faction] = None

    def __post_init__(self) -> None:
        if any(x in self.name.lower() for x in ('keep', 'castle', 'fort')):
            self.faction = Faction.get_faction_by_keep_name(self.name)

        self.icon = self.icon or GameIcon(f'{self.faction.color}_{self.type.lower()}.png')
