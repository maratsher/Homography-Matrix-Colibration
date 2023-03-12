import imgui
from app.modules.homography_matrix.float_cell_view import FloatCellView
import numpy as np


class MatrixView:

    def __init__(self, label="", height_cell=100, width_cell=100, spacing=15, shape=(3, 3),
                 flag=imgui.INPUT_TEXT_AUTO_SELECT_ALL):
        self._cells = []
        self._label = label
        self._height_cell = height_cell
        self._width_cell = width_cell
        self._shape = shape
        self._flag = flag
        self._spacing = spacing

        self._init_cells()

    def _init_cells(self):
        for i in range(self._shape[0]):
            self._cells.append([])
            for j in range(self._shape[1]):
                self._cells[i].append(FloatCellView(self._label, self._height_cell, self._width_cell, flag=self._flag))

    def show(self):
        for row in self._cells:
            imgui.begin_group()
            for cell in row:
                cell.show()
                imgui.same_line(spacing=self._spacing)
            imgui.end_group()

    def get_matrix(self) -> np.ndarray:
        hm = np.zeros(self._shape)
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                hm[i][j] = self._cells[i][j].get_val()
        return hm

    def set_matrix(self, matrix: np.ndarray):
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                self._cells[i][j].set_val(matrix[i][j])

    def get_matrix_status(self) -> bool:
        s = False
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                s += self._cells[i][j].get_status()
        return s

    def set_shifts(self, matrix: np.ndarray, shift_matrix: np.ndarray):
        self.set_matrix(matrix + shift_matrix)
