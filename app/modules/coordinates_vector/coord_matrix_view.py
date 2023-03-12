import numpy as np
import imgui

from app.modules.coordinates_vector.vector3_view import Vector3View


class CoordMatrixView:

    def __init__(self, label: str, region_width: int, region_height: int, amount_start_coord: int, border=True):

        self._coords = []
        self._label = label
        self._region_width = region_width
        self._region_height = region_height
        self._amount_start_coord = amount_start_coord
        self._num_coord = 0
        self._border = border

        # init started coordinates
        self.append_coordinates(n=self._amount_start_coord)

    def show(self, label: str):
        imgui.begin_child(label, self._region_width, self._region_height, self._border)

        for vec3 in self._coords:
            vec3.show()

        imgui.end_child()

    def append_coordinates(self, n=1):
        for _ in range(n):
            self._coords.append(Vector3View(self._label))
        self._num_coord += n

    def get_matrix(self) -> np.ndarray:
        m = np.zeros((self._num_coord, 3))
        for i, vec3 in enumerate(self._coords):
            for j in range(3):
                m[i][j] = vec3.get_vector()[j]
        return m

    def set_matrix(self, matrix: np.ndarray):
        for i, vec3 in enumerate(self._coords):
            vec3.set_vector(matrix[i])

    def get_status(self) -> bool:
        return sum([vec3.get_status() for vec3 in self._coords])

    def get_num_coord(self) -> int:
        return self._num_coord
