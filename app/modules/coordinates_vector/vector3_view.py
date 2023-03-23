import imgui

from app.modules.coordinates_vector.vector import Vector
from app.modules.gui_object import GUIObject


class Vector3View(Vector, GUIObject):

    def __init__(self, label: str, default_vector: list, z_coord: int, format_view: str, flag: int):
        Vector.__init__(self)
        GUIObject.__init__(self)
        self._label = "##"+label + str(self._id)
        self._z_coord = z_coord
        self._vector = default_vector + [self._z_coord]
        self._format = format_view
        self._flag = flag
        self._changed = False

    def show(self):
        # self._vector_view = self._vector[:-1]
        # print(self._vector_view)
        self._changed, self._vector[:-1] = imgui.input_float2(
            self._label,
            *self._vector[:-1],
            self._format,
            self._flag
        )
        # self._vector[:-1] = self._vector_view
        # self._vector.append(self._z_coord)
        
    def get_changed(self):
        return self._changed

    def set_changed(self, changed: bool):
        self._changed = changed

    def set_vector(self, vector: list):
        self._vector = vector

    def get_vector(self):
        return self._vector

