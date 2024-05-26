import sys
import cv2
import argparse
import local
import regional
import hough


def process_image(imagem, algorithm, args):
    if algorithm == "local":
        return local.process(
            imagem,
            magnitudeThreshold=args.magnitude_threshold,
            requestedAngle=args.angle,
            angularThreshold=args.angular_threshold,
            reconstructionThreshold=args.reconstruction_size,
        )
    elif algorithm == "regional":
        return regional.process(imagem, threshold=args.threshold)
    elif algorithm == "global":
        return hough.process(
            imagem,
            peaks=args.peaks_amount,
            use_empty_image=args.empty_image,
            use_continuous_lines=args.continuous_lines,
            gap=args.gap,
        )
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
        help="Threshold for Regional Edge Detection",
    )
    parser.add_argument(
        "--magnitude_threshold",
        type=int,
        default=100,
        help="Magnitude for local edge detection",
    )
    parser.add_argument(
        "--angle", type=str, default="all", help="Angle for edge detection"
    )
    parser.add_argument(
        "--angular_threshold",
        type=int,
        default=20,
        help="Threshold of Angle for edge detection",
    )
    parser.add_argument(
        "--reconstruction_size",
        type=int,
        default=5,
        help="Max pixels for edge reconstruction",
    )
    parser.add_argument(
        "--gap",
        type=int,
        default=10,
        help="Gap used in global edge detection. Define the maximum distance between two points to be considered continuous.",
    )
    parser.add_argument(
        "--peaks_amount",
        type=int,
        default=5,
        help="Amount of peaks to be detected (Global Edge Detection)",
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Path to save the output image",
    )
    parser.add_argument(
        "--continuous_lines",
        action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
        help="Use continuous lines in the output (Global Edge Detection)",
    )
    parser.add_argument(
        "--empty_image",
        action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
        help="Use an empty image as base for the output (Global Edge Detection)",
    )
    args = parser.parse_args()

    input_image = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)

    if input_image is None:
        print(f"Error: Cannot load image {args.filename}")
        return 1

    final_image = process_image(input_image, args.algorithm, args)

    if args.save:
        cv2.imwrite(args.save, final_image)

    cv2.imshow("Imagem PNG", final_image)
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to close the window
            break
    cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
