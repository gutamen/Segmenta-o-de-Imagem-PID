import sys
import argparse
import cv2


def main():
    parser = argparse.ArgumentParser(description="Image processing CLI")
    parser.add_argument("filename", type=str, help="Path to the image file")
    parser.add_argument(
        "--thresholds",
        type=int,
        nargs=2,
        default=[50, 150],
        help="Thresholds for Canny edge detection (low high)",
    )
    args = parser.parse_args()

    print(args.thresholds[0], args.thresholds[1])

    input_image = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(input_image, args.thresholds[0], args.thresholds[1])

    filename_without_extension = args.filename.split(".")[0]
    filename =f"{filename_without_extension}_pp_canny.png"

    cv2.imwrite(filename, edges)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
