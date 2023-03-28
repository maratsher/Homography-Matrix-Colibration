import imgui
from app.modules.homography_matrix.cell_view import CellView
import numpy as np


class MatrixView:

    def __init__(self, label: str, height_cell: int, width_cell: int, spacing: int, shape: tuple, format_view: str,
                 def_cell_val: float, bl: int, flag: int):
        self._cells = []
        self._label = label
        self._height_cell = height_cell
        self._width_cell = width_cell
        self._shape = shape
        self._flag = flag
        self._bl = bl
        self._def_cell_val = def_cell_val
        self._format_view = format_view
        self._spacing = spacing

        self._init_cells()

    def _init_cells(self):
        for i in range(self._shape[0]):
            self._cells.append([])
            for j in range(self._shape[1]):
                self._cells[i].append(CellView(label=self._label,
                                               height=self._height_cell,
                                               width=self._width_cell,
                                               flag=self._flag,
                                               bl=self._bl,
                                               val=self._def_cell_val,
                                               format_view=self._format_view))

    def show(self):
        for row in self._cells:
            imgui.begin_group()
            for cell in row:
                imgui.begin_group()
                cell.show()
                imgui.end_group()
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

    def get_matrix_changed(self) -> bool:
        s = False
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                s += self._cells[i][j].get_changed()
        return s

    def set_shifts(self, matrix: np.ndarray, shift_matrix: np.ndarray):
        self.set_matrix(matrix + shift_matrix)
