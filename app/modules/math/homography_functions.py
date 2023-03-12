import numpy as np
import scipy.spatial.distance as ds
from array import array


def compute_result_matrix(original_matrix: np.ndarray, homography_matrix: np.ndarray, num_coords: int):
    result_matrix = []

    kx = np.dot(original_matrix, homography_matrix[0])
    ky = np.dot(original_matrix, homography_matrix[1])
    k = np.dot(original_matrix, homography_matrix[2])
    x = np.round(kx / k, num_coords)
    y = np.round(ky / k, num_coords)

    for i, j in zip(x, y):
        result_matrix.append([i, j, 1])

    return np.asarray(result_matrix), x, y


def compute_plane_for_real(real_x, real_y, num_coord):
    zeros = np.zeros((num_coord, 1))
    np_rm_x = np.asarray(real_x).reshape((num_coord, 1))
    np_rm_y = np.asarray(real_y).reshape((num_coord, 1))
    x_min = np.min(np_rm_x)
    x_max = np.max(np_rm_x)
    y_min = np.min(np_rm_y)
    y_max = np.max(np_rm_y)

    real_coords = np.hstack([np_rm_x, np_rm_y, zeros])
    x0, y0, _ = real_coords[
        ds.cdist([[x_min, y_max, 0]], real_coords)[0].argsort()[0]]
    x1, y1, _ = real_coords[
        ds.cdist([[x_max, y_max, 0]], real_coords)[0].argsort()[0]]
    x2, y2, _ = real_coords[
        ds.cdist([[x_max, y_min, 0]], real_coords)[0].argsort()[0]]
    x3, y3, _ = real_coords[
        ds.cdist([[x_min, y_min, 0]], real_coords)[0].argsort()[0]]

    line_x = array("f", [x0, x1, x2, x3, x0])
    line_y = array("f", [y0, y1, y2, y3, y0])

    return line_x, line_y


def compute_plane_for_result(res_x, res_y, num_coord):
    np_x = np.asarray(res_x).reshape((num_coord, 1))
    np_y = np.asarray(res_y).reshape((num_coord, 1))

    x_min = np.min(np_x)
    x_max = np.max(np_x)
    y_min = np.min(np_y)
    y_max = np.max(np_y)

    result_coord = np.hstack([np_x, np_y])

    x0, y0 = result_coord[
        ds.cdist([[x_min, y_max]], result_coord)[0].argsort()[0]]
    x1, y1 = result_coord[
        ds.cdist([[x_max, y_max]], result_coord)[0].argsort()[0]]
    x2, y2 = result_coord[
        ds.cdist([[x_max, y_min]], result_coord)[0].argsort()[0]]
    x3, y3 = result_coord[
        ds.cdist([[x_min, y_min]], result_coord)[0].argsort()[0]]

    line_x = array("f", [x0, x1, x2, x3, x0])
    line_y = array("f", [y0, y1, y2, y3, y0])

    return line_x, line_y
