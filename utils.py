import matplotlib.pyplot as plt
import cv2

import numpy as np


def show_img(img, title=None):
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow(title, img)
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to close the window
            break
    cv2.destroyAllWindows()


def plot_hough_sinusoids(
    accumulator, rhos, thetas, title="hough_transform_accumulator.png"
):
    plt.imshow(
        accumulator,
        cmap="hot",
        extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]],
        aspect=0.2,
    )
    plt.title("Hough Transform Accumulator")
    plt.xlabel("Theta (degrees)")
    plt.ylabel("Rho (pixels)")
    plt.colorbar()
    plt.subplots_adjust(
        left=0.1, right=0.9, top=0.9, bottom=0.1
    )  # Adjust the subplot to increase plot area
    plt.savefig(title)  # Save the plot as an image
    plt.close()  # Close the plot to free resources
