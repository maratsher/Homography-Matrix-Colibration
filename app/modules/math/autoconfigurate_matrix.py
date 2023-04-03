import numpy as np
from scipy import spatial
import datetime

from app.modules.math import calibration_map


def find_shape_corners(points):
    bb_points = find_bounding_points(points)
    nearest_point_indexes = []
    for bb_point in bb_points:
        index = find_nearest_point_index(points, bb_point)
        nearest_point_indexes.append(index)
    return nearest_point_indexes


def find_bounding_points(points):
    min_x = min(points.T[0])
    max_x = max(points.T[0])
    min_y = min(points.T[1])
    max_y = max(points.T[1])

    up_left = (min_x, max_y)
    up_right = (max_x, max_y)
    down_left = (min_x, min_y)
    down_right = (max_x, min_y)

    return up_left, up_right, down_left, down_right


def find_nearest_point_index(points, principal_point):
    distance, index = spatial.KDTree(points).query(principal_point)
    return index


def verify_configurated(img_points, obj_points, h_matrix, p_idx_config, eps):
    gt_value = obj_points[p_idx_config[0]][p_idx_config[1]]

    points = calibration_map.convert2world(img_points, h_matrix)[:, :2]

    value = points[p_idx_config[0]][p_idx_config[1]]

    return abs(gt_value - value) <= eps


def autoconfig_matrix_element(img_points, obj_points, h_matrix, h_idx_config, p_idx_config, step, eps, iter_limit=1000):
    gt_value = obj_points[p_idx_config[0]][p_idx_config[1]]

    points = calibration_map.convert2world(img_points, h_matrix)[:, :2]

    value = points[p_idx_config[0]][p_idx_config[1]]

    step = np.array([-step, step])

    h_values = np.zeros(iter_limit)
    deltas = np.zeros(iter_limit)

    iter_count = 0
    configured = False
    while not configured:
        h_matrix[h_idx_config[0]][h_idx_config[1]] += step[int(value < gt_value)]

        points = calibration_map.convert2world(img_points, h_matrix)[:, :2]
        value = points[p_idx_config[0]][p_idx_config[1]]

        configured = abs(gt_value - value) <= eps
        h_values[iter_count] = h_matrix[h_idx_config[0]][h_idx_config[1]]
        deltas[iter_count] = abs(gt_value - value)

        iter_count += 1
        if iter_count == iter_limit:
            h_matrix[h_idx_config[0]][h_idx_config[1]] = h_values[np.argmin(deltas)]
            break


def autoconfigurate_matrix(gt_img_points, gt_obj_points, H, debug=True):
    estimated_points = calibration_map.convert2world(gt_img_points, H)
    estimated_points = estimated_points[:, :2]

    indexes = find_shape_corners(estimated_points)

    img_points = gt_img_points[indexes]
    obj_points = gt_obj_points[indexes]
    estimated_points = estimated_points[indexes]

    calibration_map.write_points(img_points)
    calibration_map.write_points(obj_points)

    #start_time = datetime.datetime.now()
    config = False
    while not config:
        eps = 0.1
        # configurate matrix offsets
        autoconfig_matrix_element(img_points, obj_points, H, [0, 2], [0, 0], step=0.01, eps=eps)
        autoconfig_matrix_element(img_points, obj_points, H, [1, 2], [0, 1], step=0.01, eps=eps)

        # configurate matrix x scale
        autoconfig_matrix_element(img_points, obj_points, H, [0, 0], [1, 0], step=0.00001, eps=eps)

        middle_img_points = np.mean(img_points[2:], axis=0).reshape((1, 3))
        middle_obj_points = np.mean(obj_points[2:], axis=0).reshape((2, 1))
        autoconfig_matrix_element(middle_img_points, middle_obj_points, H, [0, 1], [0, 0], step=0.0000001, eps=eps)

        autoconfig_matrix_element(img_points, obj_points, H, [2, 1], [2, 0], step=0.00001, eps=eps)

        autoconfig_matrix_element(img_points, obj_points, H, [1, 1], [2, 1], step=0.00001, eps=eps)

        config_result = np.full(6, False, dtype=bool)
        config_result[0] = verify_configurated(img_points, obj_points, H, [0, 0], eps=eps)
        config_result[1] = verify_configurated(img_points, obj_points, H, [0, 1], eps=eps)
        config_result[2] = verify_configurated(img_points, obj_points, H, [1, 0], eps=eps)
        config_result[3] = verify_configurated(middle_img_points, middle_obj_points, H, [0, 0], eps=eps)
        config_result[4] = verify_configurated(img_points, obj_points, H, [2, 0], eps=eps)
        config_result[5] = verify_configurated(img_points, obj_points, H, [2, 1], eps=eps)

        config = np.all(config_result)

    #estimated_points = calibration_map.convert2world(img_points, H)

    return H