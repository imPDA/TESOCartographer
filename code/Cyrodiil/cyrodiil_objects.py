from app.html_map import Coordinates
from game_map.cyrodiil_datatypes import Object, ObjectType, COVENANT, PACT, DOMINION

SCROLLS = (
    Object(ObjectType.DEFENSIVE_SCROLL, 'Ni-Mohk', Coordinates(17.62, 16.88), faction=COVENANT),
    Object(ObjectType.OFFENSIVE_SCROLL, 'Alma Ruma', Coordinates(11.97, 27.16), faction=COVENANT),
    Object(ObjectType.DEFENSIVE_SCROLL, 'Chim', Coordinates(81.23, 18.01), faction=PACT),
    Object(ObjectType.OFFENSIVE_SCROLL, 'Ghartook', Coordinates(88.02, 28.29), faction=PACT),
    Object(ObjectType.DEFENSIVE_SCROLL, 'Altadoon', Coordinates(42.92, 84.09), faction=DOMINION),
    Object(ObjectType.OFFENSIVE_SCROLL, 'Mnem', Coordinates(56.85, 83.81), faction=DOMINION),
)

TEMPLES = (
    Object(ObjectType.TEMPLE, f"Scroll Temple of {s.name}", s.coordinate, faction=s.faction) for s in SCROLLS
)

KEEPS = (
    Object(ObjectType.KEEP, 'Fort Rayles', Coordinates(17.27, 32.30)),  # 1
    Object(ObjectType.KEEP, 'Fort Warden', Coordinates(23.33, 17.57)),  # 2
    Object(ObjectType.KEEP, 'Fort Glademist', Coordinates(27.48, 27.47)),  # 3
    Object(ObjectType.KEEP, 'Fort Aleswell', Coordinates(41.26, 27.38)),  # 4
    Object(ObjectType.KEEP, 'Fort Dragonclaw', Coordinates(49.39, 10.77)),  # 5
    Object(ObjectType.KEEP, 'Fort Ash', Coordinates(33.25, 42.03)),  # 6
    Object(ObjectType.OUTPOST, 'Winter\'s Peak Outpost', Coordinates(57.93, 16.23), faction=COVENANT),
    Object(ObjectType.OUTPOST, 'Bleaker\'s Outpost', Coordinates(49.64, 26.77), faction=COVENANT),
    Object(ObjectType.TOWN, 'Bruma', Coordinates(47.74, 17.23), faction=COVENANT),
    Object(ObjectType.GATE, 'Northern High Rock Gate', Coordinates(15.94, 10.22), faction=COVENANT),
    Object(ObjectType.GATE, 'Southern High Rock Gate', Coordinates(06.89, 28.515), faction=COVENANT),

    Object(ObjectType.KEEP, 'Farragut Keep', Coordinates(83.99, 32.87)),  # 1
    Object(ObjectType.KEEP, 'Arrius Keep', Coordinates(70.24, 32.22)),  # 2
    Object(ObjectType.KEEP, 'Kingscrest Keep', Coordinates(72.74, 17.88)),  # 3
    Object(ObjectType.KEEP, 'Chalman Keep', Coordinates(57.90, 27.87)),  # 4
    Object(ObjectType.KEEP, 'Blue Road Keep', Coordinates(66.22, 42.11)),  # 5
    Object(ObjectType.KEEP, 'Drakelowe Keep', Coordinates(77.54, 57.58)),  # 6
    Object(ObjectType.OUTPOST, 'Harlun\'s Outpost', Coordinates(79.52, 46.18), faction=PACT),
    Object(ObjectType.OUTPOST, 'Sejanus Outpost', Coordinates(64.52, 50.15), faction=PACT),
    Object(ObjectType.TOWN, 'Cropsford', Coordinates(68.64, 63.14), faction=PACT),
    Object(ObjectType.GATE, 'Northern Morrowind Gate', Coordinates(83.76, 11.56), faction=PACT),
    Object(ObjectType.GATE, 'Southern Morrowind Gate', Coordinates(92.77, 30.64), faction=PACT),

    Object(ObjectType.KEEP, 'Castle Black Boot', Coordinates(40.84, 77.70)),  # 1
    Object(ObjectType.KEEP, 'Castle Bloodmane', Coordinates(57.42, 77.43)),  # 2
    Object(ObjectType.KEEP, 'Castle Faregyl', Coordinates(49.23, 68.24)),  # 3
    Object(ObjectType.KEEP, 'Castle Roebeck', Coordinates(41.78, 57.43)),  # 4
    Object(ObjectType.KEEP, 'Castle Alessia', Coordinates(56.70, 56.64)),  # 5
    Object(ObjectType.KEEP, 'Castle Brindel', Coordinates(22.51, 57.15)),  # 6
    Object(ObjectType.OUTPOST, 'Nikel Outpost', Coordinates(36.00, 51.13), faction=DOMINION),
    Object(ObjectType.OUTPOST, 'Carmala Outpost', Coordinates(22.13, 49.52), faction=DOMINION),
    Object(ObjectType.TOWN, 'Vlastarus', Coordinates(30.55, 66.12), faction=DOMINION),
    Object(ObjectType.GATE, 'Eastern Elsweyr Gate', Coordinates(60.3425, 88.24), faction=DOMINION),
    Object(ObjectType.GATE, 'Western Elsweyr Gate', Coordinates(38.41, 89.17), faction=DOMINION),
)
