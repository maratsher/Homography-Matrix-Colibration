from array import array
import numpy as np
import configparser


config = configparser.ConfigParser()
config.read('app.ini')

HOMOGRAPHY_MATRIX_SHAPE = tuple(map(int, config["HOMOGRAPHY_MATRIX_WINDOW"]["Shape"].split(",")))
AMOUNT_START_COORDS = int(config["DATA_INPUT_WINDOW"]["AmountStartedCoord"])


class Stash:

    def __init__(self):

        # data window <-> plot window
        self._real_x = array("f", [0])
        self._real_y = array("f", [0])
        self._res_x = array("f", [0])
        self._res_y = array("f", [0])
        self._num_coord = 1
        self._plot_plane = False

        # data window <-> homography window
        self._origin_coords = np.zeros((AMOUNT_START_COORDS, 2))
        self._real_coords = np.zeros((AMOUNT_START_COORDS, 2))
        self._homography_matrix = np.zeros(HOMOGRAPHY_MATRIX_SHAPE)
        self._homography_matrix_changed = False

        # file workflow
        self._is_open_file = False

    def set_plot_data(self, real_x: array, real_y: array, res_x: array, res_y: array, num_coord: int,
                      plot_plane: bool):
        self._real_x = real_x
        self._real_y = real_y
        self._res_x = res_x
        self._res_y = res_y
        self._num_coord = num_coord
        self._plot_plane = plot_plane

    def get_plot_data(self) -> tuple[array, array, array, array, int, bool]:
        return self._real_x, self._real_y, self._res_x, self._res_y, self._num_coord, self._plot_plane

    def set_homography_matrix(self, homography_matrix: np.ndarray, homography_matrix_changed: bool):
        self._homography_matrix = homography_matrix
        self._homography_matrix_changed = homography_matrix_changed

    def get_homography_matrix(self) -> tuple[np.ndarray, bool]:
        return self._homography_matrix, self._homography_matrix_changed
    
    def set_real_coords(self, real_coords: np.ndarray):
        self._real_coords = real_coords
        
    def set_origin_coords(self, origin_coords: np.ndarray):
        self._origin_coords = origin_coords
        
    def get_real_coords(self):
        return self._real_coords
    
    def get_origin_coords(self):
        return self._origin_coords

    def set_is_open_file(self, f: bool):
        self._is_open_file = f

    def get_is_open_file(self) -> bool:
        return self._is_open_file
    
    
        



