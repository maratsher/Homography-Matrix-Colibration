import imgui
import numpy as np
import configparser

from app.gui.windows.window import Window
from app.gui.windows.data_input_window import DataWindow
from app.modules.homography_matrix.matrix_view import MatrixView
from app.stash import Stash

config = configparser.ConfigParser()
config.read('app.ini')

HOMOGRAPHY_MATRIX_SHAPE = tuple(map(int, config["HOMOGRAPHY_MATRIX_WINDOW"]["Shape"].split(",")))
HOMOGRAPHY_MATRIX_CELL_WIDTH = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Cell_width"])
HOMOGRAPHY_MATRIX_CELL_HEIGHT = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Cell_height"])
HOMOGRAPHY_MATRIX_CELL_SPACING = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Spacing"])
HEIGHT = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Height"])
WIDTH = int(config["HOMOGRAPHY_MATRIX_WINDOW"]["Width"])


class HomographyWindow(Window):
    def __init__(self, stash: Stash):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Homography Matrix"
        self._N = 1
        self._shape = HOMOGRAPHY_MATRIX_SHAPE
        self._matrix = np.zeros(self._shape)
        self._shifts = np.zeros(self._shape)

        self._stash = stash

        self._homography_matrix = MatrixView(label="homography_matrix",
                                             height_cell=HOMOGRAPHY_MATRIX_CELL_HEIGHT,
                                             width_cell=HOMOGRAPHY_MATRIX_CELL_WIDTH,
                                             format_view="%.5f",
                                             spacing=HOMOGRAPHY_MATRIX_CELL_SPACING,
                                             shape=self._shape,
                                             bl=15,
                                             def_cell_val=0,
                                             flag=imgui.INPUT_TEXT_CTRL_ENTER_FOR_NEW_LINE)

    def _draw_content(self):
        # pin homography if opened
        if self._stash.get_is_open_file():
            self._homography_matrix.set_matrix(self._stash.get_homography_matrix()[0])
            self._matrix = self._homography_matrix.get_matrix()
            self._shifts = np.zeros(self._shape)
            self._stash.set_is_open_file(False)
        
        imgui.text("Homography Matrix")
        self._homography_matrix.show()

        s1, self._shifts[0] = imgui.slider_float3(
            "##slider1", *self._shifts[0],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s2, self._shifts[1] = imgui.slider_float3(
            "##slider2", *self._shifts[1],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s3, self._shifts[2] = imgui.slider_float3(
            "##slider3", *self._shifts[2],
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

        if s1 or s2 or s3:
            self._homography_matrix.set_shifts(self._matrix, self._shifts)

        if self._homography_matrix.get_matrix_changed():
            self._stash.set_homography_matrix(self._homography_matrix.get_matrix(),
                                              self._homography_matrix.get_matrix_changed())

