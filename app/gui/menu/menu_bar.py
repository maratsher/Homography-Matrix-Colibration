import imgui
from app.utils.data_loader import DataLoader
from app.stash import Stash


class MenuBar:

    def __init__(self, stash: Stash):
        self._press_new = False
        self._press_open = False
        self._press_save = False
        self._press_save_as = False
        self._stash = stash
        self._dl = DataLoader()

    def draw(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu('File', True):
                self._press_new, _ = imgui.menu_item('New', 'Ctrl+Shift+N', False, True)
                self._press_open, _ = imgui.menu_item('Open', 'Ctrl+Shift+O', False, True)
                self._press_save, _ = imgui.menu_item('Save', 'Ctrl+Shift+S', False, True)
                self._press_save_as, _ = imgui.menu_item('Save As', 'Ctrl+Shift+S', False, True)
                imgui.end_menu()

        if self._press_new:
            self._dl.new()
            self._press_new = False

        if self._press_open:
            if data := self._dl.open():
                original_coords, real_coords, homography_matrix = data
                self._stash.set_origin_coords(original_coords)
                self._stash.set_real_coords(real_coords)
                self._stash.set_homography_matrix(homography_matrix, True)
                self._stash.set_is_open_file(True)
            self._press_open = False

        if self._press_save_as:
            self._dl.save_as(self._stash.get_origin_coords(), self._stash.get_real_coords(),
                             self._stash.get_homography_matrix()[0])
            self._press_save_as = False

        if self._press_save:
            self._dl.save(self._stash.get_origin_coords(), self._stash.get_real_coords(),
                          self._stash.get_homography_matrix()[0])

            self._press_save_as = False

        imgui.end_main_menu_bar()
        