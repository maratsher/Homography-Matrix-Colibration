import imgui
import numpy as np
import configparser
from array import array

from app.gui.windows.window import Window
from app.modules.coordinates_vector.coord_matrix_view import CoordMatrixView
from app.modules.math.homography_functions import compute_result_matrix
from app.stash import Stash


config = configparser.ConfigParser()
config.read('app.ini')

HOMOGRAPHY_MATRIX_SHAPE = tuple(map(int, config["HOMOGRAPHY_MATRIX_WINDOW"]["Shape"].split(",")))
REGION_WIDTH = int(config["DATA_INPUT_WINDOW"]["Region_width"])
REGION_HEIGHT = int(config["DATA_INPUT_WINDOW"]["Region_height"])
AMOUNT_START_COORD = int(config["DATA_INPUT_WINDOW"]["AmountStartedCoord"])
HEIGHT = int(config["DATA_INPUT_WINDOW"]["Height"])
WIDTH = int(config["DATA_INPUT_WINDOW"]["Width"])
GAP_X = int(config["DATA_INPUT_WINDOW"]["Gap_x"])
GAP_Y = int(config["DATA_INPUT_WINDOW"]["Gap_y"])


class DataWindow(Window):
    def __init__(self, stash: Stash):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Input and output matrices"

        self._original_coords = CoordMatrixView(label="original coord", region_width=int(REGION_WIDTH),
                                                region_height=int(REGION_HEIGHT),
                                                amount_start_coord=int(AMOUNT_START_COORD),
                                                default_vector=[0, 0],
                                                z_coord=1,
                                                format_view="%.3f",
                                                flag=0,
                                                border=False)
        self._real_coords = CoordMatrixView(label="real coord",
                                            region_width=int(REGION_WIDTH),
                                            region_height=int(REGION_HEIGHT),
                                            amount_start_coord=int(AMOUNT_START_COORD),
                                            default_vector=[0, 0],
                                            z_coord=0,
                                            format_view="%.3f",
                                            flag=0,
                                            border=False)
        self._result_coords = CoordMatrixView(label="real coord",
                                              region_width=int(REGION_WIDTH),
                                              region_height=int(REGION_HEIGHT),
                                              amount_start_coord=int(AMOUNT_START_COORD),
                                              default_vector=[0, 0],
                                              z_coord=1,
                                              format_view="%.3f",
                                              flag=0,
                                              border=False)

        self._homography_matrix = np.zeros(HOMOGRAPHY_MATRIX_SHAPE)
        self._homography_matrix_changed = False

        self._stash = stash

    def _draw_content(self):

        # get current homography matrix
        self._homography_matrix, self._homography_matrix_changed = self._stash.get_homography_matrix()
        
        # get original and real coords from files, if opened
        if self._stash.get_is_open_file():
            self._original_coords.set_matrix(self._stash.get_origin_coords())
            self._real_coords.set_matrix(self._stash.get_real_coords())

            new_nc = self._original_coords.get_num_coord() - self._result_coords.get_num_coord()
            self._result_coords.append_coordinates(new_nc)

        # draw vector2
        imgui.begin_child("##coords_region", REGION_WIDTH, REGION_HEIGHT, True)
        imgui.begin_group()
        imgui.text("Original Coordinates")
        self._original_coords.show("Original Coordinates")
        imgui.end_group()

        imgui.same_line(spacing=10)

        imgui.begin_group()
        imgui.text("Real Coordinates")
        self._real_coords.show("Real Coordinates")
        imgui.end_group()

        imgui.same_line(spacing=10)

        imgui.begin_group()
        imgui.text("Result Coordinates")
        self._result_coords.show("Result Coordinates")
        imgui.end_group()
        imgui.end_child()

        imgui.dummy(GAP_X, GAP_Y)

        # press Add coordinate button
        if imgui.button("Add coordinate"):
            self._original_coords.append_coordinates()
            self._result_coords.append_coordinates()
            self._real_coords.append_coordinates()

        if imgui.button("File menu..."):
            imgui.open_popup("menu")

        # If the original, real or homography matrix has been changed
        if self._original_coords.get_changed() or self._homography_matrix_changed or self._real_coords.get_changed():
            # compute result homography_matrix
            num_coords = self._result_coords.get_num_coord()
            result_matrix, res_x, res_y = compute_result_matrix(self._original_coords.get_matrix(),
                                                                self._homography_matrix, num_coords)

            result_matrix = result_matrix[:, :-1].astype(float)
            self._result_coords.set_matrix(result_matrix)

            # plot
            real_coord_matrix = self._real_coords.get_matrix()
            real_x = real_coord_matrix[:, 0]
            real_y = real_coord_matrix[:, 1]
            self._stash.set_plot_data(array("f", real_x), array("f", real_y), array("f", res_x), array("f", res_y),
                                      num_coords, True)

            # update stash
            self._stash.set_real_coords(self._real_coords.get_matrix()[:, :-1])
            self._stash.set_origin_coords(self._original_coords.get_matrix()[:, :-1])

