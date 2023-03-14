import imgui
import numpy as np
import configparser

from app.gui.windows.window import Window
from app.modules.coordinates_vector.coord_matrix_view import CoordMatrixView
from app.gui.windows.plot_window import PlotWindow
from app.modules.math.homography_functions import compute_result_matrix


config = configparser.ConfigParser()
config.read('app.ini')

HOMOGRAPHY_MATRIX_SHAPE = tuple(map(int, config["HOMOGRAPHY_MATRIX_WINDOW"]["Shape"].split(",")))
REGION_WIDTH = int(config["DATA_INPUT_WINDOW"]["Region_width"])
REGION_HEIGHT = int(config["DATA_INPUT_WINDOW"]["Region_height"])
AMOUNT_START_COORD = int(config["DATA_INPUT_WINDOW"]["AmountStartedCoord"])
HEIGHT = int(config["DATA_INPUT_WINDOW"]["Height"])
WIDTH = int(config["DATA_INPUT_WINDOW"]["Width"])


class DataWindow(Window):
    def __init__(self, plot_window: PlotWindow()):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Input and output matrices"

        self._original_coords = CoordMatrixView("original coord", int(REGION_WIDTH), int(REGION_HEIGHT),
                                                int(AMOUNT_START_COORD), z_coord=1)
        self._real_coords = CoordMatrixView("real coords", int(REGION_WIDTH), int(REGION_HEIGHT),
                                            int(AMOUNT_START_COORD), z_coord=0)
        self._result_coords = CoordMatrixView("result coords", int(REGION_WIDTH), int(REGION_HEIGHT),
                                              int(AMOUNT_START_COORD))

        self._homography_matrix = np.zeros(HOMOGRAPHY_MATRIX_SHAPE)
        self._homography_matrix_status = False

        self._plot_window = plot_window

    def _draw_content(self):
        imgui.text("Original Coordinates")
        self._original_coords.show("Original Coordinates")
        imgui.text("")
        imgui.text("Real Coordinates")
        self._real_coords.show("Real Coordinates")
        imgui.text("")
        imgui.text("Result Coordinates")
        self._result_coords.show("Result Coordinates")
        imgui.text("")

        # press Add coordinate button
        if imgui.button("Add coordinate"):
            self._original_coords.append_coordinates()
            self._result_coords.append_coordinates()
            self._real_coords.append_coordinates()

        # If the original homography_matrix or homography homography_matrix has been changed
        if self._original_coords.get_status() or self._homography_matrix_status:
            # compute result homography_matrix
            num_coords = self._result_coords.get_num_coord()
            result_matrix, res_x, res_y = compute_result_matrix(self._original_coords.get_matrix(),
                                                                self._homography_matrix, num_coords)

            self._result_coords.set_matrix(result_matrix)

            # plot
            real_coord_matrix = self._real_coords.get_matrix()
            real_x = real_coord_matrix[:, 0]
            real_y = real_coord_matrix[:, 1]
            self._plot_window.plot(real_x, real_y, res_x, res_y, num_coords)

    def set_homography_matrix(self, matrix: np.ndarray):
        self._homography_matrix = matrix

    def set_homography_matrix_status(self, status: bool):
        self._homography_matrix_status = status
