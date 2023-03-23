import tkinter
from tkinter import filedialog as fd
import configparser
import os
import numpy
import numpy as np

from app.gui.windows.data_input_window import DataWindow
from app.gui.windows.homography_matrix_window import HomographyWindow


config = configparser.ConfigParser()
config.read('app.ini')

ORIGIN_FN = config["DATALOADER"]["Origin_fn"]
REAL_FN = config["DATALOADER"]["Real_fn"]
HOMOGRAPHY_FN = config["DATALOADER"]["Homography_fn"]

AMOUNT_START_COORD = int(config["DATA_INPUT_WINDOW"]["AmountStartedCoord"])


class DataLoader:

    def __init__(self):
        self._path_to_projects = False

    def _show_error_window(self, error_code=0):
        if error_code == 0:
            tkinter.messagebox.showerror(title="Error code 0", message="Неверная стурткура проекта")
        if error_code == 1:
            tkinter.messagebox.showerror(title="Error code 1", message="Значения матриц должны быть float")
        if error_code == 2:
            tkinter.messagebox.showerror(title="Error code 2", message="Координат должно быть две")
        if error_code == 3:
            tkinter.messagebox.showerror(title="Error code 3", message="Размер гомографический матрицы должен быть 3x3")
        if error_code == 4:
            tkinter.messagebox.showerror(title="Error code 4", message="Такой директории не существует")
        if error_code == 5:
            tkinter.messagebox.showerror(title="Error code 4", message="Директория должна должна быть пустой")


    def _check_project_structure(self, project_path: str) -> bool:

        listdir = os.listdir(project_path)
        if len(listdir) != 3:
            return False

        if ORIGIN_FN not in listdir:
            return False

        if REAL_FN not in listdir:
            return False

        if HOMOGRAPHY_FN not in listdir:
            return False

        return True
                
    def _read_coords(self, path_to_file: str):
        # matrix = np.zeros((0, 2))
        print(path_to_file)
        with open(path_to_file, "r") as file:
            lines = file.read().splitlines()
            len_lines = len(lines)
            if len_lines <= AMOUNT_START_COORD:
                len_lines = AMOUNT_START_COORD
            matrix = np.zeros((len_lines, 2))
            for i, l in enumerate(lines):
                try:
                    coords = list(map(float, l.split(" ")))
                except ValueError:
                    self._show_error_window(1)
                    return False
                if len(coords) != 2:
                    self._show_error_window(2)
                    return False
                matrix[i] = coords
        print(matrix)
        return matrix

    def _read_homography_matrix(self, path_to_file: str):
        matrix = np.zeros((3, 3))
        with open(path_to_file, "r") as file:
            lines = file.read().splitlines()
            if len(lines) != 3:
                self._show_error_window(3)
                return False
            for i, l in enumerate(lines):
                try:
                    col = list(map(float, l.split(" ")))
                except ValueError:
                    self._show_error_window(1)
                    return False
                if len(col) != 3:
                    self._show_error_window(3)
                    return False
                matrix[i] = col
        return matrix

    def _write_matrix(self, matrix: np.ndarray, fn: str):
        with open(os.path.join(self._path_to_projects, fn), "w+") as file:
            for i in range(matrix.shape[0]):
                file.write(" ".join(str(x) for x in matrix[i]))
                file.write("\n")

    def new(self):
        self._path_to_projects = fd.askdirectory(initialdir=self._path_to_projects, title="Выберите пустую scпапку")

        if self._path_to_projects == ():
            return

        if len(os.listdir(self._path_to_projects)) != 0:
            self._show_error_window(5)
        else:
            open(os.path.join(self._path_to_projects, ORIGIN_FN), "w")
            open(os.path.join(self._path_to_projects, REAL_FN), "w")
            open(os.path.join(self._path_to_projects, HOMOGRAPHY_FN), "w")

    def open(self):
        self._path_to_projects = fd.askdirectory(initialdir=self._path_to_projects, title="Выберите проект")

        if self._path_to_projects == ():
            return False

        if not os.path.exists(self._path_to_projects):
            self._show_error_window(4)
            return False

        if self._check_project_structure(self._path_to_projects):
            if type(original_matrix := self._read_coords(os.path.join(self._path_to_projects, ORIGIN_FN))) == bool:
                return False
            if type(real_matrix := self._read_coords(os.path.join(self._path_to_projects, REAL_FN))) == bool:
                return False
            if type(homography_matrix := self._read_homography_matrix(os.path.join(self._path_to_projects,
                                                                                   HOMOGRAPHY_FN))) == bool:
                return False

            return original_matrix, real_matrix, homography_matrix

        self._show_error_window(0)
        return False

    def save_as(self, original_matrix: np.ndarray, real_matrix: np.ndarray, homography_matrix: np.ndarray):
        self._path_to_projects = fd.askdirectory(initialdir=self._path_to_projects, title="Выберите проект")

        if self._path_to_projects == ():
            return

        self._write_matrix(matrix=original_matrix, fn=ORIGIN_FN)
        self._write_matrix(matrix=real_matrix, fn=REAL_FN)
        self._write_matrix(matrix=homography_matrix, fn=HOMOGRAPHY_FN)

    def save(self, original_matrix: np.ndarray, real_matrix: np.ndarray, homography_matrix: np.ndarray):

        if not self._path_to_projects:
            self.save_as(original_matrix, real_matrix, homography_matrix)
        else:
            self._write_matrix(matrix=original_matrix, fn=ORIGIN_FN)
            self._write_matrix(matrix=real_matrix, fn=REAL_FN)
            self._write_matrix(matrix=homography_matrix, fn=HOMOGRAPHY_FN)
                



