import cv2
import numpy as np
import utils


def distance_from_line(point, line_points):
    x0, y0 = point
    x1, y1 = line_points[0]
    x2, y2 = line_points[1]
    return np.abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / np.sqrt(
        (y2 - y1) ** 2 + (x2 - x1) ** 2
    )


def find_most_distant_points(points):
    max_dist = 0
    point_A = None
    point_B = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.linalg.norm(points[i] - points[j])
            if dist > max_dist:
                max_dist = dist
                point_A = points[i]
                point_B = points[j]

    return point_A, point_B


def angle_with_centroid(centroid, point):
    vector = point - centroid
    angle = -np.arctan2(
        vector[1], vector[0]
    )  # Negate the angle for clockwise direction
    return angle


def calculate_reference_distance(points):
    x_coords = points[:, 1]
    y_coords = points[:, 0]
    width = np.max(x_coords) - np.min(x_coords)
    height = np.max(y_coords) - np.min(y_coords)
    smallest_side = min(width, height)
    return 0.2 * smallest_side


def regional_edge_processing(edge_image, threshold):
    # 2) Definimos o limiar T e duas pilhas vazias (Ab e Fe);
    points = np.argwhere(edge_image > 0)

    if len(points) < 2:
        return points

    # Find the centroid of the point set
    centroid = np.mean(points, axis=0)

    # Sort points by the angle of the vector from the centroid
    points = sorted(points, key=lambda p: angle_with_centroid(centroid, p))

    # points = sorted(points, key=lambda p: (p[1], p[0]))  # Sort points by x, then y
    B, A = find_most_distant_points(points)

    # Calculate the reference distance
    reference_distance = calculate_reference_distance(np.array(points))

    # 3) Se P define uma curva fechada empilhamos B em Ab e Fe e A em Ab. Se a curva for aberta colocamos A em Ab e B em Fe;
    first_point = points[0]
    last_point = points[-1]
    if np.linalg.norm(first_point - last_point) > reference_distance:
        # Curve is closed
        stack_Ab = [B, A]
        stack_Fe = [B]
    else:
        # Curve is open
        stack_Ab = [A]
        stack_Fe = [B]

    reps = 0
    points_amount = len(points)

    # 8) Se a pilha Ab não estiver vazia, retornamos a (4);
    while stack_Ab and reps <= 10:
        # 4) Calculamos os parâmetros da reta que passa pelos vértices no topo de Fe e no topo de Ab;
        P1, P2 = stack_Ab[-1], stack_Fe[-1]
        index_P1 = np.where((points == P1).all(axis=1))[0][0]
        index_P2 = np.where((points == P2).all(axis=1))[0][0]
        Dmax = 0
        Vmax = None

        # 5) Para todos os pontos, entre aqueles vértices obtidos em (4),
        # calculamos suas distâncias em relação à reta obtida em (4).
        # Selecionamos o ponto (Vmax), com distância (Dmax);
        for i in range(index_P1 + 1, index_P1 + points_amount):
            point = points[i % points_amount]
            dist = distance_from_line(point, (P1, P2))

            if dist > Dmax:
                Dmax = dist
                Vmax = point

            # Break the loop if we reach index_P2
            if i % points_amount == index_P2:
                break

        # 6) Se Dmax > T, empilhamos o vértice Vmax em Ab e retornamos a (4);
        if Dmax > threshold:
            stack_Ab.append(Vmax)
        # 7) Senão removemos o vértice no topo de Ab, empilhando-o em Fe;
        else:
            removed_point = stack_Ab.pop()
            stack_Fe.append(removed_point)

        reps += 1

    # 9) Caso contrário, saímos. Os vértices em Fe definem a aproximação
    # poligonal do conjunto de pontos P.
    return stack_Fe


def draw_polygons(image, points):
    for i in range(len(points) - 1):
        cv2.line(image, tuple(reversed(points[i])), tuple(reversed(points[i + 1])), 100)
    if np.all(points[0] == points[-1]):
        cv2.line(image, tuple(reversed(points[-1])), tuple(reversed(points[0])), 100)
    return image


def process(image, threshold=100, canny_threshold=(80, 150)):
    _, binary_image = cv2.threshold(image, canny_threshold[0], 255, cv2.THRESH_BINARY)

    utils.show_img(binary_image, title="Image")

    # create a new empty image
    output_image = np.zeros_like(image)

    polygon_points = regional_edge_processing(binary_image, threshold)
    image_with_polygon = draw_polygons(output_image, polygon_points)

    return image_with_polygon
