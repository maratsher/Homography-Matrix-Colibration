import imgui

from app.modules.gui_object import GUIObject


class FloatCellView(GUIObject):

    def __init__(self, label: str, height: int, width: int, val_f=0, bl=15, formats="%.5f", flag=0):
        super().__init__()
        self._label = "##"+label+str(self._id)
        self._height = height
        self._width = width
        self._format = formats
        self._bl = bl
        self._flag = flag

        self._val_s = str(val_f)
        self._val_f = val_f
        self._status = False

    def _to_float(self, val: str) -> float:
        try:
            val = float(val)
            return val
        except ValueError:
            self._val_s = str(self._val_f)
            return self._val_f

    def show(self):
        self._status, self._val_s = imgui.input_text_multiline(self._label, self._val_s, self._bl, self._width,
                                                               self._height, self._flag)
        self._val_f = self._to_float(self._val_s)

    def get_val(self) -> float:
        return self._val_f

    def set_val(self, val_f: float):
        self._val_f = val_f
        self._val_s = str(val_f)
        self._status = True

    def get_status(self) -> bool:
        return self._status

    def set_status(self, status: bool):
        self._status = status
        