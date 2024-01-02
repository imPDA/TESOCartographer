from pathlib import Path
from typing import Sequence, Any

import folium

from datatypes import Coordinate


class BasicMap(folium.Map):
    def __init__(self, path_to_map_file: Path, *, width: str | float, height: str | float):
        super().__init__(
            crs='Simple', tiles=None,

            zoom_start=20,  # does not work TODO fix
            location=(50, 50),  # does not work TODO fix

            # zoom_control=False,

            min_lat=-10,
            max_lat=110,
            min_lon=-10,
            max_lon=110,
            max_bounds=True,
            maxBoundsViscosity=1  # `maxBoundsViscosity=1.0` fully disables panning outside of map, ref. to Leaflet docs

            # min_zoom???
            # location???
        )
        if width:
            self.get_root().width = width
        if height:
            self.get_root().height = height

        self.add_overlay(path_to_map_file)

    def add_stylesheet(self, path: str, *, name: str = 'custom_css') -> None:
        self.default_css.append((name, folium.CssLink(path).url))

    def add_script(self, path: str) -> None:
        self.get_root().html.add_child(folium.JavascriptLink(path))

    def add_overlay(self, path_to_map_file: Path) -> None:  # TODO path-like
        overlay = folium.raster_layers.ImageOverlay(
            image=str(path_to_map_file),
            pixelated=False,
            bounds=[[0, 0], [100, 100]],
            zindex=1,  # is it necessary?
            control=False  # removes map layer from list in `LayerControl()` ↓
            # https://gis.stackexchange.com/questions/402190/how-to-fully-customise-layercontrol-in-folium
        )
        overlay.add_to(self)
        self.fit_bounds(bounds=[[0, 0], [100, 100]])

    def iframe(self, *, width: int = None, height: int = None):
        if width:
            self.get_root().width = f"{width}px"
        if height:
            self.get_root().height = f"{height}px"

        return self.get_root()._repr_html_()  # noqa

    def add_marker(
            self,
            coordinate: Coordinate,
            popup: folium.Popup | str | None = None,
            tooltip: folium.Tooltip | str | None = None,
            icon: folium.Icon | None = None,
            draggable: bool = False,
            **kwargs: str | float | bool | Sequence | dict | None
    ) -> None:
        folium.Marker(
            location=[100 - coordinate.y, coordinate.x],
            popup=popup,
            tooltip=tooltip,
            icon=icon,
            draggable=draggable,
            **kwargs
        ).add_to(self)

    def add_multiple_to_header(self, objects: Any) -> None:
        for obj in objects:
            self.get_root().header.add_child(obj)
