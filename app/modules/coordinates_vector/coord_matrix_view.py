import numpy as np
import imgui

from app.modules.coordinates_vector.vector3_view import Vector3View


class CoordMatrixView:

    def __init__(self, label: str, region_width: int, region_height: int, amount_start_coord: int,
                 default_vector: list, z_coord: int, format_view: str, flag: int, border: bool):

        self._coords = []
        self._label = label
        self._region_width = region_width
        self._region_height = region_height
        self._amount_start_coord = amount_start_coord
        self._default_vector = default_vector
        self._z_coord = z_coord
        self._num_coord = 0
        self._format_view = format_view
        self._flag = flag
        self._border = border

        # init started coordinates
        self.append_coordinates(n=self._amount_start_coord)

    def show(self, label: str):
        imgui.push_item_width(200)
        for vec3 in self._coords:
            vec3.show()
        imgui.pop_item_width()

    def append_coordinates(self, n=1):
        for _ in range(n):
            self._coords.append(Vector3View(self._label, default_vector=self._default_vector, z_coord=self._z_coord,
                                            format_view=self._format_view, flag=self._flag))
        self._num_coord += n

    def get_matrix(self) -> np.ndarray:
        m = np.zeros((self._num_coord, 3))
        for i, vec3 in enumerate(self._coords):
            for j in range(3):
                m[i][j] = vec3.get_vector()[j]
        return m

    def set_matrix(self, matrix: np.ndarray):
        
        # if not enough cells for setting coords
        if matrix.shape[0] > self._num_coord:
            diff = matrix.shape[0] - self._num_coord
            self.append_coordinates(diff)

        for i, vec3 in enumerate(self._coords):
            vec3.set_vector(np.append(matrix[i], [self._z_coord]))

    def get_changed(self) -> bool:
        return sum([vec3.get_changed() for vec3 in self._coords])

    def get_num_coord(self) -> int:
        return self._num_coord
