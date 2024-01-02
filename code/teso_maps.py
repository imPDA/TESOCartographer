import json
from pathlib import Path

import folium
import folium.plugins as plugins

from base import BasicMap
from datatypes import Icon, Coordinate, MapObject, MapObjectType, Lorebook


base_dir = Path.cwd().parent
PATH_TO_ICONS = base_dir / 'static/img/icons'
PATH_TO_MAPPINS_DATA = base_dir / 'static/mappins/mappins_output_1_96_2.json'


def get_objects_from_mappins(
        path_to_mappins_data: Path,
        mappins_name: str,
        object_name: str,
        teso_location_name: str,
        icon_filename: str
) -> list[MapObject]:
    with open(path_to_mappins_data, 'r', encoding='utf-8') as f:
        mappins_data = json.load(f)

    return [
        MapObject(
            MapObjectType(object_name),
            Coordinate(obj[0] * 100, obj[1] * 100),
            Icon(PATH_TO_ICONS / icon_filename),
            f"{object_name} #{i}"
        ) for i, obj in enumerate(mappins_data[mappins_name][teso_location_name], start=1)
    ]


class TESOMap(BasicMap):
    def __init__(self, location_name: str, path_to_map_file: Path, width: int, height: int):
        super().__init__(path_to_map_file, width=width, height=height)
        self.location_name = location_name

    def add_collection(self, name: str, objects: list[MapObject], icon_size: int | str) -> None:
        group = folium.FeatureGroup(name=f"{name}", overlay=False, show=False).add_to(self)

        for obj in objects:
            icon = folium.features.CustomIcon(
                obj.icon.filename,
                icon_size=(icon_size, icon_size),
                icon_anchor=(int(icon_size / 2), int(icon_size / 2))
            )

            group.add_child(folium.Marker(
                (100 - obj.coordinate.y, obj.coordinate.x),
                icon=icon,
                tooltip=folium.Tooltip(obj.name, sticky=False, direction='bottom', permanent=True),
            ))

        # plugins.GroupedLayerControl(
        #     groups={f"{name}": [group, ]},
        #     exclusive_groups=False,
        #     collapsed=False,
        # ).add_to(self)

    def add_lorebooks(self, path: str | Path, icon_size: int):
        with open(path, 'r', encoding='utf-8') as f:
            mappins_data = json.load(f)

        lorebooks_data = mappins_data['Lorebooks'][self.location_name.lower()]
        lorebooks = [
            Lorebook(
                coordinate=Coordinate(data[0] * 100, data[1] * 100),
                icon=Icon(PATH_TO_ICONS / 'lorebook.png'),
                some_number_1=data[2],
                some_number_2=data[3]
            ) for i, data in enumerate(lorebooks_data, start=1)
        ]

        group = folium.FeatureGroup(name="Lorebooks", overlay=False).add_to(self)  # show=False,

        grouped_lorebooks = {}
        for lorebook in lorebooks:
            grouped_lorebooks.setdefault(lorebook.some_number_2, []).append(lorebook)

        subgroups = []
        for some_number_2, group_of_lorebooks in sorted(grouped_lorebooks.items()):
            subgroup = plugins.FeatureGroupSubGroup(group, name=f"[{some_number_2}] ...", show=False).add_to(self)
            for lorebook in group_of_lorebooks:
                icon = folium.features.CustomIcon(
                    lorebook.icon.filename,
                    icon_size=(icon_size, icon_size),
                    icon_anchor=(int(icon_size / 2), int(icon_size / 2))
                )

                lorebook_name = f"[{lorebook.some_number_2}] {lorebook.some_number_1}"

                subgroup.add_child(folium.Marker(
                    (100 - lorebook.coordinate.y, lorebook.coordinate.x),
                    icon=icon,
                    tooltip=folium.Tooltip(lorebook_name, sticky=False, direction='bottom', permanent=True),
                ))
            subgroups.append(subgroup)

        plugins.GroupedLayerControl(
            groups={"Lorebooks": subgroups},
            exclusive_groups=False,
            collapsed=False,
        ).add_to(self)

    def fill_from_mappins(self, path_to_mappins_data: str | Path) -> None:
        self.add_collection(
            'Skyshards',
            get_objects_from_mappins(path_to_mappins_data, 'SkyShards', 'Skyshard', self.location_name.lower(), 'skyshard.png'),
            25
        )

        self.add_lorebooks(path_to_mappins_data, 18)

        # self.add_collection(
        #     'Lorebooks',
        #     get_objects_from_mappins(
        #         path_to_mappins_data,
        #         'Lorebooks',
        #         'Lorebook',
        #         self.location_name.lower(),
        #         'lorebook.png'
        #     ),
        #     18
        # )

        self.add_collection(
            'Treasures',
            get_objects_from_mappins(path_to_mappins_data, 'TreasureMaps', 'Treasure', self.location_name.lower(), 'red_x_mark.png'),
            25
        )

    def save(self, path: Path):
        super().save(path / f'{self.location_name}.html')


def map_fabric(location_name, path_to_map_file, path_to_output: Path = None) -> None:
    location_map = TESOMap(location_name, path_to_map_file, 300, 300)
    location_map.fill_from_mappins(PATH_TO_MAPPINS_DATA)

    location_map.add_stylesheet('map_style.css')
    location_map.add_multiple_to_header([
        folium.Link('<link rel="preconnect" href="https://fonts.googleapis.com">'),
        folium.Link('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'),
        folium.Link('<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">')
    ])

    folium.LayerControl(collapsed=False).add_to(location_map)

    if not path_to_output:
        path_to_output = path_to_map_file.parent / 'output'

    location_map.save(path_to_output)


if __name__ == '__main__':
    maps_to_create = [
        ('Deshaan', base_dir / 'static/img/maps/deshaan_2048_2048.png'),
    ]
    for map_ in maps_to_create:
        map_fabric(*map_)
