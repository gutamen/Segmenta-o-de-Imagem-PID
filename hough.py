import numpy as np
import cv2
import matplotlib
import utils

matplotlib.use("Agg")  # Use the Agg backend


def hough_transform(edge_image):
    # 2) Defina como o plano rho/theta será dividido (estrutura da matriz acumuladora);
    height, width = edge_image.shape
    max_dist = int(np.sqrt(height**2 + width**2))

    rho_range = 2 * max_dist
    theta_range = 180

    thetas = np.deg2rad(np.arange(-90.0, 90.0))
    rhos = np.linspace(-max_dist, max_dist, rho_range)
    accumulator = np.zeros((rho_range, theta_range), dtype=np.int32)

    # 3) Aplique a parametrização aos pontos da imagem das bordas, atualizando a matriz acumuladora;
    y_idxs, x_idxs = np.nonzero(edge_image)

    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(len(thetas)):
            # rho = x * cos(theta) + y * sin(theta)
            rho = int(x * np.cos(thetas[t_idx]) + y * np.sin(thetas[t_idx]))
            accumulator[rho + max_dist, t_idx] += 1

    return accumulator, thetas, rhos, max_dist


def find_peaks(accumulator, threshold=100):
    peaks = []
    rho_indices, theta_indices = np.where(accumulator >= threshold)
    for rho_idx, theta_idx in zip(rho_indices, theta_indices):
        peaks.append((rho_idx, theta_idx))
    return peaks

def draw_lines(image, line_segments):
    for line in line_segments:
        for i in range(len(line) - 1):
            cv2.line(image, line[i], line[i + 1], 255, 2)

    return image

def is_continuous(line_segments, min_length=30, gap=10):
    continuous_lines = []

    for line in line_segments:
        if len(line) > min_length:
            continuous_lines.append(line)

    return continuous_lines


def get_line_segments(edge_image, peaks, theta, max_dist):
    line_segments = []

    for peak in peaks:
        rho_idx, theta_idx = peak
        rho = rho_idx - max_dist
        theta_val = theta[theta_idx]

        a = np.cos(theta_val)
        b = np.sin(theta_val)
        points = []

        for x in range(edge_image.shape[1]):
            y = int((rho - x * a) / b)
            if 0 <= y < edge_image.shape[0]:
                if edge_image[y, x] > 0:
                    points.append((x, y))

        if points:
            line_segments.append(points)

    return line_segments

# def draw_lines(image, peaks, theta, max_dist):
#     for peak in peaks:
#         rho_idx, theta_idx = peak
#         rho = rho_idx - max_dist
#         theta_val = theta[theta_idx]

#         a = np.cos(theta_val)
#         b = np.sin(theta_val)
#         x0 = a * rho
#         y0 = b * rho

#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))

#         cv2.line(image, (x1, y1), (x2, y2), 255, 2)

#     return image


def process(in_image, threshold=80):
    utils.show_img(in_image, title="Input image")
    
    # create an empty output image
    image_with_lines = np.zeros_like(in_image)

    accumulator, thetas, rhos, max_dist = hough_transform(in_image)

    # 4) Examine a matriz acumuladora em busca de células com valores elevados;
    peaks = find_peaks(accumulator, threshold=threshold)
    line_segments = get_line_segments(in_image, peaks, thetas, max_dist)

    print(f"Found {len(line_segments)} line segments")
    print(line_segments)

    continuous_lines = is_continuous(line_segments)

    image_with_lines = draw_lines(image_with_lines, continuous_lines)
    # image_with_lines = draw_lines(image_with_lines, peaks, thetas, max_dist)

    utils.plot_hough_sinusoids(
        accumulator, rhos, thetas, title="hough_transform_accumulator.png"
    )

    return image_with_lines
