import sys
import cv2
import argparse
import local
import regional
import hough


def process_image(imagem, algorithm):
    if algorithm == "local":
        return local.process(imagem)
    elif algorithm == "regional":
        return regional.process(imagem)
    elif algorithm == "global":
        return hough.process(imagem)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Image processing CLI")
    parser.add_argument("filename", type=str, help="Path to the image file")
    parser.add_argument(
        "algorithm",
        type=str,
        choices=["local", "regional", "global"],
        help="Image processing algorithm",
    )
    args = parser.parse_args()

    input_image = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)

    if input_image is None:
        print(f"Error: Cannot load image {args.filename}")
        return 1

    final_image = process_image(input_image, args.algorithm)

    cv2.imshow("Imagem PNG", final_image)
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to close the window
            break
    cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
