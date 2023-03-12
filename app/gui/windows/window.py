from __future__ import annotations

import imgui


class Window:
    def __init__(self, window_width=300, window_height=200):
        super().__init__()
        self._x = 0
        self._y = 0

        self._width = window_width
        self._height = window_height

    @property
    def position(self):
        return imgui.Vec2(self._x, self._y)

    @property
    def size(self):
        return imgui.Vec2(self._width, self._height)

    @staticmethod
    def screen2window(window: Window, screen_x: float, screen_y: float):
        return imgui.Vec2(screen_x - window._x, screen_y - window._y)

    @staticmethod
    def window2screen(window: Window, window_x: float, window_y: float):
        return imgui.Vec2(window_x + window._x, window_y + window._y)

    def _draw_content(self):
        pass

    def _draw_overlay(self):
        pass

    def _begin_window(self):
        imgui.set_next_window_size(self.size.x, self.size.y, imgui.FIRST_USE_EVER)
        #imgui.set_next_window_position(self.position.x, self.position.y, imgui.FIRST_USE_EVER)
        imgui.begin(self._id)

    def _end_window(self):
        imgui.end()

    def _init_window(self):
        pass

    def _handle_input(self):
        pass

    def draw(self):
        self._init_window()
        self._begin_window()
        self._draw_content()
        self._draw_overlay()
        self._handle_input()
        self._end_window()


if __name__ == "__main__":
    pass
