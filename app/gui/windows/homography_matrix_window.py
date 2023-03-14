import imgui
import numpy as np
import configparser

from app.gui.windows.window import Window
from app.gui.windows.data_input_window import DataWindow
from app.modules.homography_matrix.matrix_view import MatrixView

config = configparser.ConfigParser()
config.read('app.ini')

HOMOGRAPHY_MATRIX_SHAPE = tuple(map(int, config["HOMOGRAPHY_MATRIX_WINDOW"]["Shape"].split(",")))
HOMOGRAPHY_MATRIX_CELL_WIDTH = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Cell_width"])
HOMOGRAPHY_MATRIX_CELL_HEIGHT = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Cell_height"])
HOMOGRAPHY_MATRIX_CELL_SPACING = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Spacing"])
HEIGHT = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Height"])
WIDTH = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Width"])


class HomographyWindow(Window):
    def __init__(self, data_window: DataWindow):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Homography Matrix"
        self._N = 1
        self._shape = HOMOGRAPHY_MATRIX_SHAPE
        self._cell_height = HOMOGRAPHY_MATRIX_CELL_HEIGHT
        self._cell_width = HOMOGRAPHY_MATRIX_CELL_WIDTH
        self._spacing = HOMOGRAPHY_MATRIX_CELL_SPACING
        self._matrix = np.zeros(self._shape)
        self._shifts = np.zeros(self._shape)
        self._data_window = data_window

        self._homography_matrix = MatrixView("c", self._cell_height, self._cell_width, self._spacing, self._shape)

    def _draw_content(self):
        imgui.text("Homography Matrix")
        self._homography_matrix.show()

        s1, self._shifts[0] = imgui.slider_float3(
            "s1", *self._shifts[0],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s2, self._shifts[1] = imgui.slider_float3(
            "s2", *self._shifts[1],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s3, self._shifts[2] = imgui.slider_float3(
            "s3", *self._shifts[2],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        imgui.text("")

        imgui.begin_group()
        if imgui.button("Применить"):
            self._matrix = self._homography_matrix.get_matrix()
            self._shifts = np.zeros(self._shape)
        imgui.end_group()

        imgui.same_line(spacing=5)

        imgui.begin_group()
        if imgui.button("Сбросить"):
            self._homography_matrix.set_matrix(self._matrix)
            self._shifts = np.zeros(self._shape)
        imgui.end_group()

        imgui.same_line(spacing=5)

        imgui.begin_group()
        if imgui.button("Очистить"):
            self._matrix = np.zeros(self._shape)
            self._homography_matrix.set_matrix(np.zeros(self._shape))
            self._shifts = np.zeros(self._shape)
        imgui.end_group()

        # self._matrix = self.hm.get_homography_matrix()

        if s1 or s2 or s3:
            self._homography_matrix.set_shifts(self._matrix, self._shifts)
        
        self._data_window.set_homography_matrix(self._homography_matrix.get_matrix())
        self._data_window.set_homography_matrix_status(self._homography_matrix.get_matrix_status())

        # imgui.text('You wrote: %' + str(list(self._matrix)))

    def get_matrix(self):
        return self._matrix

    def set_matrix(self, matrix: np.ndarray):
        self._matrix = matrix

    def set_n(self, n: float):
        self._N = n
