from app.app import ImGuiApp
from app.gui.windows.data_input_window import DataWindow
from app.gui.windows.homography_matrix_window import HomographyWindow
from app.gui.windows.plot_window import PlotWindow
from app.stash import Stash

import imgui


class Homography(ImGuiApp):
    def __init__(self, window_width, window_height, fullscreen):
        super().__init__(window_width, window_height, fullscreen)

        self._stash = Stash()
        self.plot_window = PlotWindow(self._stash)
        self.data_window = DataWindow(self._stash)
        self.homography_window = HomographyWindow(self._stash)

    def draw_content(self):
        self.data_window.draw()
        self.homography_window.draw()
        self.plot_window.draw()

if __name__ == "__main__":
    app = Homography(1740, 735, fullscreen=False)
    app.run()
