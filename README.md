# Edge Detection

This repository contains a program that implements three methods for global edge detection, specifically designed for the digital image processing discipline. The base algorithms used in this program are comprehensively explained in the `Segmentacao de Imagens.pdf` file included in the repository. Specifically:

- The **Local Edge Detection** algorithm is detailed on page 42.
- The **Regional Edge Detection** algorithm is discussed on page 47.
- The **Global Edge Detection** algorithm is explained on page 54.

This documentation provides in-depth insights and theoretical background on the implementation and functioning of each algorithm.

## Overview

The program processes images using three different algorithms for edge detection:
1. **Local Edge Detection**
2. **Regional Edge Detection**
3. **Global Edge Detection**

Each algorithm can be customized using various parameters to achieve the desired edge detection results.

## Features

- **Local Edge Detection**: Utilizes magnitude and angle thresholds for precise edge detection.
- **Regional Edge Detection**: Applies a threshold to the entire image for regional edge detection.
- **Global Edge Detection**: Implements the Hough Transform to detect edges globally, with options for peak detection, continuous lines, and using an empty image as the base.

### Arguments

- `<filename>`: Path to the image file.
- `<algorithm>`: The edge detection algorithm to use (`local`, `regional`, `global`).

### Options

- `--threshold`: Threshold for Regional Edge Detection (default: 100).
- `--magnitude_threshold`: Magnitude for Local Edge Detection (default: 100).
- `--angle`: Angle for Local Edge Detection (default: "all").
- `--angular_threshold`: Threshold of Angle for Local Edge Detection (default: 20).
- `--reconstruction_size`: Max pixels for edge reconstruction in Local Edge Detection (default: 5).
- `--gap`: Gap used in Global Edge Detection to define the maximum distance between two points to be considered continuous (default: 10).
- `--peaks_amount`: Amount of peaks to be detected in Global Edge Detection (default: 5).
- `--save`: Path to save the output image.
- `--continuous_lines`: Use continuous lines in the output for Global Edge Detection (default: False).
- `--empty_image`: Use an empty image as the base for the output in Global Edge Detection (default: False).

## Usage

### Command Line Interface

The program provides a command-line interface (CLI) for ease of use. Below is the main structure of the command to run the program:

### Local
```bash
 python main.py images/tijolo.png local
```

```bash
 python main.py images/tijolo.png local --angle 90 --magnitude_threshold 150
```

### Regional

### Global
```bash
python3 main.py images/global/shapes_pp_canny.png global --peaks 12 --save images/global/output_shapes.png
```

```bash
python3 main.py images/global/shapes_pp_canny.png global --peaks 2 --empty_image --continuous_lines --save images/global/output_shapes.png
```

## Preprocessing Input Images

The expected input image for the edge detection program should be preprocessed. To facilitate this, we provide a preprocessing script, `canny.py`, which applies Canny edge detection to the input image.

### Canny Edge Detection Preprocessing

The `canny.py` script processes an image using the Canny edge detection method and saves the preprocessed image for further use in the main edge detection program.

### Usage

### Command Line Interface

The script provides a command-line interface (CLI) for ease of use. Below is the main structure of the command to run the preprocessing script:

```bash
python canny.py <filename> [options]
```

### Arguments

- `<filename>`: Path to the image file.

### Options

- `--thresholds`: Thresholds for Canny edge detection (low, high) (default: [50, 150]).
