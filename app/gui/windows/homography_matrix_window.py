import imgui
import numpy as np
import configparser

from app.gui.windows.window import Window
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
GAP_X = int(config["DATA_INPUT_WINDOW"]["Gap_x"])
GAP_Y = int(config["DATA_INPUT_WINDOW"]["Gap_y"])


class HomographyWindow(Window):
    def __init__(self, stash: Stash):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Homography Matrix"
        self._interval = 1
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

        # show homography matrix view
        self._homography_matrix.show()

        imgui.dummy(GAP_X, GAP_Y)

        # press clean button
        if imgui.button("Clean",  width=120, height=0):
            self._homography_matrix.set_matrix(np.zeros(HOMOGRAPHY_MATRIX_SHAPE))

        # if homography matrix
        if self._homography_matrix.get_matrix_changed():
            self._stash.set_homography_matrix(self._homography_matrix.get_matrix(),
                                              self._homography_matrix.get_matrix_changed())