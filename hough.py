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


def find_peaks_by_amount(accumulator, num_peaks=10):
    # Flatten the accumulator array and sort it by value in descending order
    flat_accumulator = accumulator.flatten()
    sorted_indices = np.argsort(flat_accumulator)[::-1]

    # Get the indices of the top num_peaks values
    top_indices = sorted_indices[:num_peaks]

    # Convert the flat indices back to the 2D indices of the accumulator
    peaks = [np.unravel_index(idx, accumulator.shape) for idx in top_indices]

    return peaks


def draw_lines(image, line_segments):
    for line in line_segments:
        for i in range(len(line) - 1):
            cv2.line(image, line[i], line[i + 1], 255, 1)

    return image


def get_line_segments(edge_image, peaks, thetas, max_dist):
    line_segments = []

    # Get the coordinates of all edge points
    y_idxs, x_idxs = np.nonzero(edge_image)

    for peak in peaks:
        rho_idx, theta_idx = peak
        rho = rho_idx - max_dist
        theta = thetas[theta_idx]

        a = np.cos(theta)
        b = np.sin(theta)

        points = []
        for x, y in zip(x_idxs, y_idxs):
            calculated_rho = int(x * a + y * b)
            if calculated_rho == rho:
                points.append((x, y))

        if points:
            line_segments.append(points)

    return line_segments


def is_continuous(line_segments, max_gap=10):
    continuous_lines = []

    for line in line_segments:
        if not line:
            continue

        current_segment = [line[0]]
        for i in range(1, len(line)):
            if np.linalg.norm(np.array(line[i]) - np.array(line[i - 1])) <= max_gap:
                current_segment.append(line[i])
            else:
                if (
                    len(current_segment) > 1
                ):  # Ensure the segment has more than one point
                    continuous_lines.append(current_segment)
                current_segment = [
                    line[i]
                ]  # Start a new segment with the current point

        if (
            len(current_segment) > 1
        ):  # Add the last segment if it has more than one point
            continuous_lines.append(current_segment)

    return continuous_lines


def process(in_image, peaks=5, use_empty_image=True, use_continuous_lines=False, gap=10):
    # create an empty output image
    base_iamge = np.zeros_like(in_image) if use_empty_image else in_image

    accumulator, thetas, rhos, max_dist = hough_transform(in_image)

    # 4) Examine a matriz acumuladora em busca de células com valores elevados;
    peaks = find_peaks_by_amount(accumulator, num_peaks=peaks)

    lines = get_line_segments(in_image, peaks, thetas, max_dist)

    if use_continuous_lines:
        lines = is_continuous(lines, max_gap=gap)

    final_image = draw_lines(base_iamge, lines)

    utils.plot_hough_sinusoids(
        accumulator, rhos, thetas, title="hough_transform_accumulator.png"
    )

    return final_image
