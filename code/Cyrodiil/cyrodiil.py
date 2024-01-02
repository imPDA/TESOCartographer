import os
from pathlib import Path

import folium

from datatypes import Coordinate
from base import BasicMap
from cyrodiil_objects import SCROLLS, TEMPLES, KEEPS

PATH_TO_MAP = f'{os.getcwd()}/static/img/full_map_5120x5120.png'
PATH_TO_ICONS = Path.cwd() / 'static/img/icons'


class CyrodiilMap(BasicMap):
    def __init__(
            self,
            path_to_map_file: str = PATH_TO_MAP,
            *,
            width,
            height,
            size_of_keeps: int = 12,
            size_of_resources: int = 10
    ):
        super().__init__(path_to_map_file, width=width, height=height)

        self.size_of_keeps = size_of_keeps
        self.size_of_resources = size_of_resources

        self._add_temples()
        self._add_scrolls()
        self._add_keeps()
        self._add_resources()

        self._first_icon = True

        self.get_root().render()

    def _calculate_y_anchor(self, size: int) -> int:
        # It helps to deal with icon bug: all icons except the first one are translated along y-axis. Icon anchor must
        # be `self.size_of_keeps / 2` for all icon but in reality it is `self.size_of_keeps / 2` for the first one and `self.size_of_keeps` for all others

        return int(size / 2)

        if self._first_icon:
            self._first_icon = False
            return int(size / 2)
        else:
            return size

    def _add_temples(self):
        for temple in TEMPLES:
            icon = folium.features.CustomIcon(
                f"{PATH_TO_ICONS}/temples/{temple.icon.filename}",
                icon_size=(self.size_of_keeps, self.size_of_keeps),
                icon_anchor=(int(self.size_of_keeps / 2), self._calculate_y_anchor(self.size_of_keeps))
            )

            self.add_marker(
                temple.coordinate.x, temple.coordinate.y,
                tooltip=temple.name,
                icon=icon
            )

    def _add_scrolls(self):
        for i, scroll in enumerate(SCROLLS):
            icon = folium.features.CustomIcon(
                f"{PATH_TO_ICONS}/scrolls/{scroll.icon.filename}",
                icon_size=(self.size_of_keeps, self.size_of_keeps),
                icon_anchor=(int(self.size_of_keeps / 2), self._calculate_y_anchor(self.size_of_keeps))
            )

            self.add_marker(
                scroll.coordinate.x, scroll.coordinate.y,
                tooltip=scroll.name,
                icon=icon
            )

    def _add_keeps(self):
        for i, keep in enumerate(KEEPS):
            icon = folium.features.CustomIcon(
                f"{PATH_TO_ICONS}/keeps/{keep.icon.filename}",
                icon_size=(self.size_of_keeps, self.size_of_keeps),
                icon_anchor=(int(self.size_of_keeps / 2), self._calculate_y_anchor(self.size_of_keeps))
            )

            self.add_marker(
                keep.coordinate.x, keep.coordinate.y,
                tooltip=keep.name,
                icon=icon
            )

    def _add_resources(self):
        with open(f'{os.getcwd()}/game_map/resources.txt', 'r') as f:
            resources_raw = f.read()

        # with open('resources.txt', 'r') as f:
        #     resources_raw = f.read()

        for i, resource_raw in enumerate(resources_raw.splitlines()):
            keep, type_of_resource, coordinates_raw = resource_raw.split(',')
            resource_name = f"{keep.strip()} {type_of_resource.strip()}"
            resource_coordinates = Coordinate(*map(float, coordinates_raw.split('x')))
            if 'Keep' in keep:
                color = 'red'
            elif 'Castle' in keep:
                color = 'yellow'
            else:
                color = 'blue'

            icon = folium.features.CustomIcon(
                f"{PATH_TO_ICONS}/resources/{color}_{type_of_resource.strip().lower()}.png",
                icon_size=(self.size_of_resources, self.size_of_resources),
                icon_anchor=(int(self.size_of_resources / 2), self._calculate_y_anchor(self.size_of_resources))
            )

            self.add_marker(
                resource_coordinates.x, resource_coordinates.y,
                tooltip=resource_name,
                icon=icon
            )
