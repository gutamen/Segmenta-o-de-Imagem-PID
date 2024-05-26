import cv2
import numpy as np


def correction(image, rad, reconstructionThreshold):
    height, widht = image.shape[:2]
    if 1.5 <= rad <= 1.6:
        for i in range(0, height):
            k = 0
            hole = False
            start = True
            for j in range(0, widht):
                if image[i][j] > 0 and not hole:
                    start = False
                elif image[i][j] == 0 and not start:
                    k += 1
                    hole = True
                    if k > reconstructionThreshold:
                        start = True
                        hole = False
                        k = 0
                elif image[i][j] > 0 and hole:
                    hole = False
                    for l in range(k, 0, -1):
                        image[i][j - l] = 255
                    k = 0

    #   ângulo de 0º ou 180º
    elif rad == 0 or (3.13 <= rad <= 3.15):
        for i in range(0, widht):
            k = 0
            hole = False
            start = True
            for j in range(0, height):
                if image[j][i] > 0 and not hole:
                    start = False
                elif image[j][i] == 0 and not start:
                    k += 1
                    hole = True
                    if k > reconstructionThreshold:
                        start = True
                        hole = False
                        k = 0
                elif image[j][i] > 0 and hole:
                    hole = False
                    for l in range(k, 0, -1):
                        image[j - l][i] = 255
                    k = 0

    #  ângulo de 45º
    elif 0.75 <= rad <= 0.8:
        for i in range(widht - 1, -1, -1):
            j = height - 1
            l = i
            k = 0
            hole = False
            start = True
            while j >= 0 and l < widht:
                if image[j][l] > 0 and not hole:
                    start = False
                elif image[j][l] == 0 and not start:
                    k += 1
                    hole = True
                    if k > reconstructionThreshold:
                        start = True
                        hole = False
                        k = 0
                elif image[j][l] > 0 and hole:
                    hole = False
                    for t in range(k, 0, -1):
                        image[j + t][l - t] = 255
                    k = 0
                j -= 1
                l += 1

        if height > 1:
            for i in range(height - 2, -1, -1):
                j = i
                l = 0
                k = 0
                hole = False
                start = True
                while j >= 0 and l < widht:
                    if image[j][l] > 0 and not hole:
                        start = False
                    elif image[j][l] == 0 and not start:
                        k += 1
                        hole = True
                        if k > reconstructionThreshold:
                            start = True
                            hole = False
                            k = 0
                    elif image[j][l] > 0 and hole:
                        hole = False
                        for t in range(k, 0, -1):
                            image[j + t][l - t] = 255
                        k = 0
                    j -= 1
                    l += 1

    #  ângulo de 135º
    elif 2.3 <= rad <= 2.4:
        for i in range(widht - 1, -1, -1):
            j = 0
            l = i
            k = 0
            hole = False
            start = True
            while j < height and l < widht:
                if image[j][l] > 0 and not hole:
                    start = False
                elif image[j][l] == 0 and not start:
                    k += 1
                    hole = True
                    if k > reconstructionThreshold:
                        start = True
                        hole = False
                        k = 0
                elif image[j][l] > 0 and hole:
                    hole = False
                    for t in range(k, 0, -1):
                        image[j - t][l - t] = 255
                    k = 0
                j += 1
                l += 1

        if height > 1:
            for i in range(1, height, 1):
                j = i
                l = 0
                k = 0
                hole = False
                start = True
                while j < height and l < widht:
                    if image[j][l] > 0 and not hole:
                        start = False
                    elif image[j][l] == 0 and not start:
                        k += 1
                        hole = True
                        if k > reconstructionThreshold:
                            start = True
                            hole = False
                            k = 0
                    elif image[j][l] > 0 and hole:
                        hole = False
                        for t in range(k, 0, -1):
                            image[j - t][l - t] = 255
                        k = 0
                    j += 1
                    l += 1

    return image


def process(
    image,
    magnitudeThreshold=80,
    requestedAngle="all",
    angularThreshold=10,
    reconstructionThreshold=20,
):
    image = cv2.GaussianBlur(image, (5, 5), 0)
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    if requestedAngle == "0":
        requestedAngle = [0, 180]
    elif requestedAngle == "45":
        requestedAngle = [45]
    elif requestedAngle == "90":
        requestedAngle = [90]
    elif requestedAngle == "135":
        requestedAngle = [135]
    elif requestedAngle == "all":
        requestedAngle = [0, 45, 90, 135, 180]
    else:
        print("Invalid Angle")
        return image

    # Valores
    #    magnitudeThreshold = 80    # entre 0 e 255
    #    angularThreshold = 10       # ângulo necessário para considerar na linha

    # Calcular a magnitude e a direção do gradiente
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    direction = np.arctan2(grad_y, grad_x)
    height, widht = image.shape[:2]

    for i in range(0, height - 1):
        for j in range(0, widht - 1):
            if direction[i][j] < 0:
                direction[i][j] += np.pi

    rad = np.deg2rad(requestedAngle)
    radThreshold = np.deg2rad(angularThreshold)

    image = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    images = []

    for i in range(0, len(rad)):
        images.append(image.copy())

    for l in range(0, len(rad)):
        for i in range(0, height):
            for j in range(0, widht):
                if image[i][j] >= magnitudeThreshold and (
                    rad[l] - radThreshold <= direction[i][j] <= rad[l] + radThreshold
                ):
                    images[l][i][j] = 255
                else:
                    images[l][i][j] = 0

        images[l] = correction(images[l], rad[l], reconstructionThreshold)

    returnImage = images[0]
    for i in range(1, len(images)):
        returnImage = np.maximum(images[i], returnImage)

    return returnImage


"""
    anguloRotacao = 45
    centro = (widht // 2, height // 2)
    heightRotacionada = int(widht * np.abs(np.sin(np.radians(anguloRotacao))) + height * np.abs(np.cos(np.radians(anguloRotacao))))
    widhtRotacionada = int(height * np.abs(np.sin(np.radians(anguloRotacao))) + widht * np.abs(np.cos(np.radians(anguloRotacao))))
    matrizRotacao = cv2.getRotationMatrix2D(centro, anguloRotacao, 1.0)
    matrizRotacao[0, 2] += (widhtRotacionada - widht) / 2
    matrizRotacao[1, 2] += (heightRotacionada - height) / 2

    centro = (widhtRotacionada // 2, heightRotacionada // 2)
    magnitude = cv2.warpAffine(magnitude, matrizRotacao, (widhtRotacionada, heightRotacionada), borderMode = cv2.BORDER_CONSTANT, borderValue = (0), flags=cv2.INTER_NEAREST)        
    print(magnitude.shape[:2])
    matrizRotacaoInversa = cv2.getRotationMatrix2D(centro, -anguloRotacao, 1.0)

    magnitude = cv2.warpAffine(magnitude, matrizRotacaoInversa, (widhtRotacionada, heightRotacionada), flags=cv2.INTER_NEAREST)       
    
    mid_x, mid_y = int(widhtRotacionada/2), int(heightRotacionada/2)
    cw2, ch2 = int(widht/2), int(height/2)

    return magnitude[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
"""
