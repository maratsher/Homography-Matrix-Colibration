import imgui
import numpy as np
import configparser

from app.gui.windows.window import Window
from app.modules.homography_matrix.matrix_view import MatrixView
from app.stash import Stash
from app.modules.math.autoconfigurate_matrix import autoconfigurate_matrix

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
        self._eps = 0.1

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
            self._stash.set_is_open_file(False)

        # show homography matrix view
        self._homography_matrix.show()

        imgui.dummy(GAP_X, GAP_Y)

        imgui.text("Epsilon:")
        imgui.same_line(spacing=7)
        imgui.push_item_width(70)
        _, self._eps = imgui.input_float("##epsilon_input_float", value=self._eps, format="%.3f")
        imgui.pop_item_width()

        imgui.dummy(GAP_X, GAP_Y)

        # press auto config button
        if imgui.button("Auto config",  width=120, height=0):
            original_matrix = self._stash.get_origin_coords()
            real_matrix = self._stash.get_real_coords()
            curr_homography_matrix = self._stash.get_homography_matrix()[0]
            original_matrix = np.concatenate((original_matrix, np.ones((original_matrix.shape[0], 1))), axis=1)
            try:
                new_homography_matrix = autoconfigurate_matrix(original_matrix, real_matrix, curr_homography_matrix,
                                                               self._eps)
                self._homography_matrix.set_matrix(new_homography_matrix)
            except IndexError:
                print("Can not config matrix")

        imgui.same_line(spacing=3)

        # press clean button
        if imgui.button("Clean",  width=120, height=0):
            self._homography_matrix.set_matrix(np.zeros(HOMOGRAPHY_MATRIX_SHAPE))

        # if homography matrix changed
        if self._homography_matrix.get_matrix_changed():
            self._stash.set_homography_matrix(self._homography_matrix.get_matrix(),
                                              self._homography_matrix.get_matrix_changed())