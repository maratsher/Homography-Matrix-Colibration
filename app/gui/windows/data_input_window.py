import imgui
import numpy as np
import configparser
from array import array

from app.gui.windows.window import Window
from app.modules.coordinates_vector.coord_matrix_view import CoordMatrixView
from app.modules.math.homography_functions import compute_result_matrix
from app.stash import Stash
from app.utils.data_loader import DataLoader
from app.modules.math.compute_error import compute_average_error



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
        self._error = np.nan

        self._stash = stash

        # TO DO
        self._unsaved = ""
        self._dl = DataLoader()

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
        if imgui.button("Add coordinate", width=120, height=0):
            self._original_coords.append_coordinates()
            self._result_coords.append_coordinates()
            self._real_coords.append_coordinates()

        imgui.dummy(3, 3)

        imgui.text("Error: "+str(self._error))

        imgui.dummy(GAP_X, GAP_Y)
        imgui.separator()
        imgui.dummy(GAP_X, GAP_Y)

        if imgui.button("Open", width=120, height=0):
            imgui.open_popup("open")

        imgui.same_line(spacing=3)

        if imgui.button("Save", width=120, height=0):
            if self._dl.path_to_projects != "":
                imgui.open_popup("save")
            else:
                imgui.open_popup("save_as")

        imgui.same_line(spacing=3)

        if imgui.button("Save As", width=120, height=0):
            imgui.open_popup("save_as")

        imgui.text("Current project: "+self._unsaved+self._dl.path_to_projects)

        # open modal window
        if imgui.begin_popup_modal("open", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
            imgui.text("Path to project dir")
            _, self._dl.path_to_projects = imgui.input_text("##open_input", self._dl.path_to_projects)

            if imgui.button(label="OK", width=120, height=0):
                if data := self._dl.open():
                    original_coords, real_coords, homography_matrix = data
                    self._original_coords.set_matrix(original_coords)
                    self._real_coords.set_matrix(real_coords)
                    self._stash.set_homography_matrix(homography_matrix, True)
                    self._stash.set_is_open_file(True)
                    imgui.close_current_popup()
                else:
                    self._dl.path_to_projects = ""

            imgui.set_item_default_focus()
            imgui.same_line()

            if imgui.button(label="Cancel", width=120, height=0):
                imgui.close_current_popup()

            imgui.end_popup()

        # save modal window
        if imgui.begin_popup_modal("save", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
            self._dl.save(self._stash.get_origin_coords(), self._stash.get_real_coords(),
                          self._stash.get_homography_matrix()[0])
            self._unsaved = ""
            imgui.close_current_popup()
            imgui.end_popup()

        # save_as modal window
        if imgui.begin_popup_modal("save_as", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
            imgui.text("Path to path dir")
            _, self._dl.path_to_projects = imgui.input_text("##save_as_input", self._dl.path_to_projects)

            if imgui.button(label="OK", width=120, height=0):
                self._dl.save_as(self._stash.get_origin_coords(), self._stash.get_real_coords(),
                                 self._stash.get_homography_matrix()[0])
                self._unsaved = ""
                imgui.close_current_popup()

            imgui.set_item_default_focus()
            imgui.same_line()

            if imgui.button(label="Cancel", width=120, height=0):
                imgui.close_current_popup()

            imgui.end_popup()

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
            self._homography_matrix_changed = False

            # compute error
            real_coord_matrix = real_coord_matrix[:, :-1].astype(float)
            self._error = compute_average_error(real_coord_matrix, result_matrix)
