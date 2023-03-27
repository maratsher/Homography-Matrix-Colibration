import imgui
import configparser
import os
import numpy as np


config = configparser.ConfigParser()
config.read('app.ini')

ORIGIN_FN = config["DATALOADER"]["Origin_fn"]
REAL_FN = config["DATALOADER"]["Real_fn"]
HOMOGRAPHY_FN = config["DATALOADER"]["Homography_fn"]

AMOUNT_START_COORD = int(config["DATA_INPUT_WINDOW"]["AmountStartedCoord"])


class DataLoader:

    def __init__(self):
        self.path_to_projects = ""

    @staticmethod
    def show_error_window(error_code=0):
        
        if error_code == 0:
            imgui.open_popup("error0")
            if imgui.begin_popup_modal("error0", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Неверная стурткура проекта")
                imgui.end_popup()
        if error_code == 1:
            imgui.open_popup("error1")
            if imgui.begin_popup_modal("error1", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Значения матриц должны быть float")
                imgui.end_popup()
        if error_code == 2:
            imgui.open_popup("error2")
            if imgui.begin_popup_modal("error2", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Координат должно быть две")
                imgui.end_popup()
        if error_code == 3:
            imgui.open_popup("error3")
            if imgui.begin_popup_modal("error3", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Размер гомографический матрицы должен быть 3x3")
                imgui.end_popup()
        if error_code == 4:
            imgui.open_popup("error4")
            if imgui.begin_popup_modal("error4", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Такой директории не существует")
                imgui.end_popup()
        if error_code == 5:
            imgui.open_popup("error5")
            if imgui.begin_popup_modal("error5", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
                imgui.text("Директория должна должна быть пустой")
                imgui.end_popup()

    def _check_project_structure(self) -> bool:

        listdir = os.listdir(self.path_to_projects)
        if len(listdir) != 3:
            return False

        if ORIGIN_FN not in listdir:
            return False

        if REAL_FN not in listdir:
            return False

        if HOMOGRAPHY_FN not in listdir:
            return False

        return True
                
    def _read_coords(self, fn: str):
        with open(os.path.join(self.path_to_projects,fn), "r") as file:
            lines = file.read().splitlines()
            len_lines = len(lines)
            if len_lines <= AMOUNT_START_COORD:
                len_lines = AMOUNT_START_COORD
            matrix = np.zeros((len_lines, 2))
            for i, l in enumerate(lines):
                try:
                    coords = list(map(float, l.split(" ")))
                except ValueError:
                    DataLoader.show_error_window(1)
                    return False
                if len(coords) != 2:
                    DataLoader.show_error_window(2)
                    return False
                matrix[i] = coords
        return matrix

    def _read_homography_matrix(self, fn: str):
        matrix = np.zeros((3, 3))
        with open(os.path.join(self.path_to_projects, fn), "r") as file:
            lines = file.read().splitlines()
            if len(lines) != 3:
                DataLoader.show_error_window(3)
                return False
            for i, l in enumerate(lines):
                try:
                    col = list(map(float, l.split(" ")))
                except ValueError:
                    DataLoader.show_error_window(1)
                    return False
                if len(col) != 3:
                    DataLoader.show_error_window(3)
                    return False
                matrix[i] = col
        return matrix

    def _write_matrix(self, matrix: np.ndarray, fn: str):
        with open(os.path.join(self.path_to_projects, fn), "w+") as file:
            for i in range(matrix.shape[0]):
                file.write(" ".join(str(x) for x in matrix[i]))
                file.write("\n")

    # def new(self):
    #     self.path_to_projects = fd.askdirectory(initialdir=self.path_to_projects, title="Выберите пустую scпапку")
    # 
    #     if self.path_to_projects == ():
    #         return
    # 
    #     if len(os.listdir(self.path_to_projects)) != 0:
    #         DataLoader.show_error_window(5)
    #     else:
    #         open(os.path.join(self.path_to_projects, ORIGIN_FN), "w")
    #         open(os.path.join(self.path_to_projects, REAL_FN), "w")
    #         open(os.path.join(self.path_to_projects, HOMOGRAPHY_FN), "w")

    def open(self):

        if self.path_to_projects == "":
            return False

        if not os.path.exists(self.path_to_projects):
            DataLoader.show_error_window(4)
            return False

        if self._check_project_structure():
            if type(original_matrix := self._read_coords(ORIGIN_FN)) == bool:
                return False
            if type(real_matrix := self._read_coords(REAL_FN)) == bool:
                return False
            if type(homography_matrix := self._read_homography_matrix(HOMOGRAPHY_FN)) == bool:
                return False

            print(original_matrix, real_matrix, homography_matrix)

            return original_matrix, real_matrix, homography_matrix

        DataLoader.show_error_window(0)
        return False

    def save_as(self, original_matrix: np.ndarray, real_matrix: np.ndarray, homography_matrix: np.ndarray):

        if self.path_to_projects == ():
            return

        self._write_matrix(matrix=original_matrix, fn=ORIGIN_FN)
        self._write_matrix(matrix=real_matrix, fn=REAL_FN)
        self._write_matrix(matrix=homography_matrix, fn=HOMOGRAPHY_FN)

    def save(self, original_matrix: np.ndarray, real_matrix: np.ndarray, homography_matrix: np.ndarray):

        if not self.path_to_projects:
            self.save_as(original_matrix, real_matrix, homography_matrix)
        else:
            self._write_matrix(matrix=original_matrix, fn=ORIGIN_FN)
            self._write_matrix(matrix=real_matrix, fn=REAL_FN)
            self._write_matrix(matrix=homography_matrix, fn=HOMOGRAPHY_FN)
