from app.app import ImGuiApp
from app.gui.windows.data_input_window import DataWindow
from app.gui.windows.homography_matrix_window import HomographyWindow
from app.gui.windows.plot_window import PlotWindow
from app.gui.menu.menu_bar import MenuBar
from app.stash import Stash


class Homography(ImGuiApp):
    def __init__(self, window_width, window_height, fullscreen):
        super().__init__(window_width, window_height, fullscreen)

        self._stash = Stash()
        self.menu_bar = MenuBar(self._stash)
        self.plot_window = PlotWindow(self._stash)
        self.data_window = DataWindow(self._stash)
        self.homography_window = HomographyWindow(self._stash)

    def draw_content(self):
        self.data_window.draw()
        self.homography_window.draw()
        self.plot_window.draw()
        self.menu_bar.draw()


if __name__ == "__main__":
    app = Homography(1280, 860, fullscreen=False)
    app.run()
