import imgui
import itertools

from app.modules.coordinates_vector.vector import Vector


class Vector3View(Vector):
    __id_iter = itertools.count()

    def __init__(self, label: str, default_val=[0, 0, 0], format_view="%.2f", flag=0):
        super().__init__(vector=default_val)
        self._id = str(next(self.__id_iter))
        self._label = label + str(self._id)
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
