import imgui
from imgui import plot as implot
import configparser
from array import array


from app.gui.windows.window import Window
from app.modules.math.homography_functions import compute_plane_for_real, compute_plane_for_result
from app.stash import Stash


config = configparser.ConfigParser()
config.read('app.ini')

HEIGHT = int(config["PLOT_WINDOW"]["Height"])
WIDTH = int(config["PLOT_WINDOW"]["Width"])


class PlotWindow(Window):
    def __init__(self, stash: Stash):
        super().__init__(WIDTH, HEIGHT)
        self._id = "Plotting"
        self._real_x = array("f", [0])
        self._real_y = array("f", [0])
        self._res_x = array("f", [0])
        self._res_y = array("f", [0])
        self._num_coord = 1
        self._plot_plane = False

        self._stash = stash

    def _draw_content(self):

        # get current data
        self._real_x, self._real_y, self._res_x, self._res_y, self._num_coord, self._plot_plane\
            = self._stash.get_plot_data()

        w, h = imgui.get_window_size()
        implot.begin_plot("plot", size=(w-30, h-30))

        # plot scatter
        implot.push_colormap(1)
        implot.plot_scatter2("result coord", self._res_x, self._res_y, self._num_coord)
        implot.plot_scatter2("real coord", self._real_x, self._real_y, self._num_coord)
        implot.pop_colormap()

        # plot plane
        if self._plot_plane:

            implot.push_colormap(1)
            # plot real plane
            line_x, line_y = compute_plane_for_real(self._real_x, self._real_y, self._num_coord)
            implot.plot_line2("real plane", line_x, line_y, 5)

            # plot result plane
            line_x, line_y = compute_plane_for_result(self._res_x, self._res_y, self._num_coord)
            implot.plot_line2("result plane", line_x, line_y, 5)
            implot.pop_colormap()

        implot.end_plot()
