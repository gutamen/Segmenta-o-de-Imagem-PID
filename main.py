import PIL
import cv2
import numpy as np

imagem = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)
#imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
#imagem = cv2.GaussianBlur(imagem, (5, 5), 0)
#_, imagem = cv2.threshold(imagem, 127, 255, cv2.THRESH_BINARY)

# Calcular o gradiente nas direções x e y
grad_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)

# Calcular a magnitude e a direção do gradiente
magnitude = np.sqrt(grad_x**2 + grad_y**2)
direcao = np.arctan2(grad_y, grad_x)

magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

cv2.imshow('Imagem PNG', magnitude_normalizada)
cv2.waitKey(0)
cv2.destroyAllWindows()

#np.savetxt('imagem_binaria.txt', imagem/255, fmt='%d')
#print(imagem/255)

"""
def mark_faults(binary_image, threshold_M, threshold_alpha, alpha, Ta, K):
    # Etapa 1: Calcula as matrizes M(x, y) e alfa(x, y)
    M = cv2.moments(binary_image)
    x_c = int(M["m10"] / M["m00"])
    y_c = int(M["m01"] / M["m00"])
    alfa = np.arctan2(y_c, x_c)  # Direção angular

    # Etapa 2: Cria a imagem binária g(x, y)
    rows, cols = binary_image.shape
    g = np.zeros((rows, cols), dtype=np.uint8)
    for x in range(rows):
        for y in range(cols):
            if M[x, y] > threshold_M and np.abs(alfa - alpha) <= Ta:
                g[x, y] = 1

    # Etapa 3: Marca as falhas
    for x in range(rows):
        for y in range(cols):
            if g[x, y] == 0:
                continue
            # Verifica se é uma falha
            if x > 0 and g[x-1, y] == 0 and x < rows-1 and g[x+1, y] == 0:
                count_zeros = 0
                for k in range(-K, K+1):
                    if y + k < 0 or y + k >= cols:
                        continue
                    if g[x, y+k] == 0:
                        count_zeros += 1
                if count_zeros <= K:
                    g[x, y] = 0

    return g



threshold_M = 1
threshold_alpha = 0.5
alpha = 0
Ta = 0.1
K = 1

"""

