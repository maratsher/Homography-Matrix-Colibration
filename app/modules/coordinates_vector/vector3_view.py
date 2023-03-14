import imgui
import itertools

from app.modules.coordinates_vector.vector import Vector
from app.modules.gui_object import GUIObject


class Vector3View(Vector, GUIObject):

    def __init__(self, label: str, default_val=[0, 0, 0], format_view="%.2f", flag=0):
        Vector.__init__(self, vector=default_val)
        GUIObject.__init__(self)
        self._label = "##"+label + str(self._id)
        self._format = format_view
        self._flag = flag
        self._status = False

    def show(self):
        self._status, self._vector = imgui.input_float3(
            self._label,
            *self._vector,
            self._format,
            self._flag
        )
        
    def get_status(self):
        return self._status

    def set_status(self, status: bool):
        self._status = status
