import imgui

class MenuBar:

    def __init__(self):
        self._press_new = False
        self._press_open = False
        self._press_save = False


    def draw(self):
        if imgui.begin_main_menu_bar():
        # first menu dropdown
            if imgui.begin_menu('File', True):
                self._press_new, _ = imgui.menu_item('New', 'Ctrl+N', False, True)
                self._press_open, _ = imgui.menu_item('Open', 'Ctrl+O', False, True)
                self._press_save, _ = imgui.menu_item('Save', 'Ctrl+S', False, True)
                imgui.end_menu()

        imgui.end_main_menu_bar()
        