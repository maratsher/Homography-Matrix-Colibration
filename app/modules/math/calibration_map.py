import numpy as np
import pickle
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


def load_centroid_columns():
    with open('points.p', 'rb') as f:
        return pickle.load(f)


def generate_img_points(centroids_sets):
    a = []
    for columns_set in centroids_sets:
        for column in columns_set:
            for reflector in column:
                a.append([reflector.center[0], reflector.center[1], 1])
    return np.array(a)


def generate_obj_points(centroids_sets, k=1):
    x_vector = []
    y_vector = []
    for columns_set in centroids_sets:
        for column in columns_set:
            for reflector in column:
                x_vector.append(reflector.world_pos[0] * k)
                y_vector.append(reflector.world_pos[1] * k)
    return np.array([x_vector, y_vector]).T


def write_points(points):
    for point in points:
        point_list = list(map(str, point.tolist()))
        print("WRITE POINTS")
        print(", ".join(point_list))


def point_to_world(point2d, h_matrix):
    point3d = np.dot(h_matrix, np.array([point2d[0], point2d[1], 1]))
    return point3d[0] / point3d[2], point3d[1] / point3d[2], 0


# def plot_map(a, b, x):
#     positions = []
#     for pos in a:
#         positions.append(point_to_world(pos, x))
#     positions = np.array(positions)
#
#     plt.scatter(positions.T[0], positions.T[1], c='red')
#     plt.scatter(b.T[0], b.T[1], alpha=0.7)
#     plt.show()


def convert2world(img_points, h_matrix):
    obj_points = np.dot(h_matrix, img_points.T).T
    vector = obj_points[:, 2:]
    return np.vstack([(obj_points / vector)[:, :2].T, np.zeros(len(obj_points))]).T


# def plot_map_3d(h_matrix, camera_pos=None):
#     figure = plt.figure()
#     axis = Axes3D(figure)
#
#     y_grid = np.linspace(0, 1080, 21)
#     x_grid = np.linspace(0, 1920, 21)
#
#     img_points = []
#     for y in y_grid:
#         for x in x_grid:
#             img_points.append([x, y, 1])
#
#     positions = convert2world(np.array(img_points), h_matrix)
#
#     axis.scatter(positions.T[0], positions.T[1])
#
#     if camera_pos is not None:
#         axis.scatter(camera_pos[0], camera_pos[1], camera_pos[2])
#
#     plt.show()


def calculate_average_error(img_points, obj_points, h_matrix):
    estimated_obj_points = convert2world(img_points, h_matrix)[:, :2]
    diff = np.abs(estimated_obj_points - obj_points)
    return np.mean(diff, axis=0)


def calculate_projective_matrix(img_points, obj_points):
    rough_matrix = np.linalg.lstsq(img_points, obj_points, rcond=-1)[0]
    projective_matrix = np.ones((3, 3))
    projective_matrix[0:1] = rough_matrix.T[0]
    projective_matrix[1:2] = rough_matrix.T[1]
    projective_matrix[2:3] = np.array([0, 0, 1])
    return projective_matrix


def calculate_scale_factors(real_points, estimated_points):
    estimated_points = estimated_points[:, :2]
    scale_factors = np.zeros(len(estimated_points))
    for i in range(len(estimated_points)):
        a = np.array([[estimated_points[i][0]], [estimated_points[i][1]]])
        b = np.array(real_points[i])
        k = np.linalg.lstsq(a, b, rcond=-1)[0]
        scale_factors[i] = k
    return scale_factors


def calculate_rough_matrix(img_points, obj_points, debug=True):
    projective_matrix = calculate_projective_matrix(img_points, obj_points)
    print("\npre-projective matrix: \n", projective_matrix)

    estimated_obj_points = np.dot(projective_matrix, img_points.T).T
    print("\nestimated obj pos: \n", estimated_obj_points)

    scale_factors = 1 / calculate_scale_factors(obj_points, estimated_obj_points)

    print("\nscale factors: ", scale_factors)
    print("\nscale factors test: \n", (estimated_obj_points.T / scale_factors).T)

    matrix_scale_string = np.linalg.lstsq(img_points, scale_factors, rcond=-1)[0]
    estimated_scale_factors = np.dot(matrix_scale_string, img_points.T).T

    updated_img_points = (img_points.T / estimated_scale_factors).T
    print("\nupdated image points: \n", np.around(updated_img_points, 3))

    projective_matrix = calculate_projective_matrix(updated_img_points, estimated_obj_points)
    projective_matrix[2:3] = matrix_scale_string

    print("\nprojective matrix: \n", projective_matrix)

    print("\nconvert to world test:\n", convert2world(img_points, projective_matrix))

    print("\naverage error: ", calculate_average_error(img_points, obj_points, projective_matrix))

    return projective_matrix
