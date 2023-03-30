import imgui

from app.modules.gui_object import GUIObject


class CellView(GUIObject):

    def __init__(self, label: str, height: int, width: int, val: float, bl: int, format_view: str, flag: int):
        super().__init__()
        self._label = "##" + label + str(self._id)
        self._height = height
        self._width = width
        self._format = format_view
        self._bl = bl
        self._flag = flag

        self._mantissa, self._exponent = self._to_exp(val)
        self._val = val
        self._changed = False

    def _to_exp(self, val: float) -> (float, int):
        exp_str = "{0:.8E}".format(val)
        m_e = exp_str.split("E")
        return float(m_e[0]), int(m_e[1])

    def _to_std(self, mantissa: float, exponent: int) -> float:
        return mantissa * pow(10, exponent)

    def show(self):
        imgui.text("e = "+str(self._exponent))
        imgui.same_line(spacing=150)
        imgui.text("+")
        if click1:=imgui.is_item_clicked(0):
            self._exponent += 1
        imgui.same_line(spacing=5)
        imgui.text("-")
        if click2:=imgui.is_item_clicked(0):
            self._exponent -= 1
        imgui.push_item_width(200)
        self._changed, self._mantissa = imgui.drag_float(self._label, self._mantissa,
                                                         change_speed=pow(10, self._exponent),
                                                         #change_speed=0.01,
                                                         min_value=-1, max_value=1, format='%.8f')
        imgui.pop_item_width()

        if click1 or click2:
            self._changed = True

        self._val = self._to_std(mantissa=self._mantissa, exponent=self._exponent)

    def get_val(self) -> float:
        return self._val

    def set_val(self, val: float):
        self._val = val
        self._mantissa, self._exponent = self._to_exp(self._val)
        self._changed = True

    def get_changed(self) -> bool:
        return self._changed

    def set_changed(self, changed: bool):
        self._changed = changed
