import imgui

from app.modules.coordinates_vector.vector import Vector
from app.modules.gui_object import GUIObject


class Vector3View(Vector, GUIObject):

    def __init__(self, label: str, default_val=[0, 0], z_coord=0, format_view="%.2f", flag=0):
        Vector.__init__(self, vector=default_val+[z_coord])
        GUIObject.__init__(self)
        self._label = "##"+label + str(self._id)
        self._vector_view = default_val
        self._z_coord = z_coord
        self._format = format_view
        self._flag = flag
        self._status = False

    def show(self):
        self._vector_view = self._vector[:-1]
        print(self._vector_view)
        self._status, self._vector_view = imgui.input_float2(
            self._label,
            *self._vector_view,
            self._format,
            self._flag
        )
        self._vector = list(self._vector_view)
        self._vector.append(self._z_coord)
        
    def get_status(self):
        return self._status

    def set_status(self, status: bool):
        self._status = status
