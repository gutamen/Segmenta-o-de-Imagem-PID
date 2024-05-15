import sys
import cv2
import argparse
import local
import regional
import hough


def process_image(imagem, algorithm, args):
    if algorithm == "local":
        return local.process(imagem, limiarMagnitude = args.magnitudeThreshold, anguloSolicitado = args.angle, limiarAngular = args.angularThreshold, limiarReconstrucao = args.reconstructionSize)
    elif algorithm == "regional":
        return regional.process(imagem, threshold=args.threshold)
    elif algorithm == "global":
        return hough.process(imagem, threshold=args.threshold)
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
    parser.add_argument(
        "--threshold",
        type=int,
        default=100,
        help="Threshold for Hough Transform peak detection",
    )

    parser.add_argument(
        "--magnitudeThreshold",
        type=int,
        default=100,
        help='Magnitude for local edge detection'
    )

    parser.add_argument(
        "--angle",
        type=str,
        default='todos',
        help='Angle for edge detection'
    )

    parser.add_argument(
        "--angularThreshold",
        type=int,
        default=20,
        help='Threshold of Angle for edge detection'
    )

    parser.add_argument(
        "--reconstructionSize",
        type=int,
        default=5,
        help='Max pixels for edge reconstruction'
    )

    args = parser.parse_args()

    input_image = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)
    

    if input_image is None:
        print(f"Error: Cannot load image {args.filename}")
        return 1

    final_image = process_image(input_image, args.algorithm, args)

    cv2.imshow("Imagem PNG", final_image)
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to close the window
            break
    cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
