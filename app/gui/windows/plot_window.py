from imgui import plot as implot
import configparser
from array import array


from app.gui.windows.window import Window
from app.modules.math.homography_functions import compute_plane_for_real, compute_plane_for_result


config = configparser.ConfigParser()
config.read('app.ini')

HEIGHT = int(config["PLOT_WINDOW"]["Height"])
WIDTH = int(config["PLOT_WINDOW"]["Width"])

class PlotWindow(Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Plotting"
        self._real_x = array("f", [0])
        self._real_y = array("f", [0])
        self._res_x = array("f", [0])
        self._res_y = array("f", [0])
        self._num_coord = 1
        self._plot_plane = False

    def _draw_content(self):
        implot.begin_plot("plot")

        # plot scatter
        implot.plot_scatter2("result coord", self._res_x, self._res_y, self._num_coord)
        implot.plot_scatter2("real coord", self._real_x, self._real_y, self._num_coord)

        # plot plane
        if self._plot_plane:

            # plot real plane
            line_x, line_y = compute_plane_for_real(self._real_x, self._real_y, self._num_coord)
            implot.plot_line2("real plane", line_x, line_y, 5)

            # plot result plane
            line_x, line_y = compute_plane_for_result(self._res_x, self._res_y, self._num_coord)
            implot.plot_line2("result plane", line_x, line_y, 5)

        implot.end_plot()

    def plot(self, rm_x, rm_y, x, y, num_coord):
        self._real_x = array("f", rm_x)
        self._real_y = array("f", rm_y)
        self._res_x = array("f", x)
        self._res_y = array("f", y)
        self._num_coord = num_coord
        self._plot_plane = True
