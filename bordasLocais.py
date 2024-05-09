import PIL
import cv2
import numpy as np

def bordasLocais(imagem, limiarMagnitude = 80, anguloSolicitado = 0, limiarAngular = 10):
    grad_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)


    # Valores
#    limiarMagnitude = 80    # entre 0 e 255
#    anguloSolicitado = 0
#    limiarAngular = 10       # ângulo necessário para considerar na linha
    

    # Calcular a magnitude e a direção do gradiente
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    direcao = np.arctan2(grad_y, grad_x)
    altura, largura = imagem.shape[:2]

    for i in range(0, altura - 1):
        for j in range(0, largura - 1):
            if(direcao[i][j] < 0):
                direcao[i][j] += np.pi

    rad = np.deg2rad(anguloSolicitado)
    limiarRad = np.deg2rad(limiarAngular)


    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    for i in range(0, altura - 1):
        for j in range(0, largura - 1):
            if magnitude[i][j] >= limiarMagnitude and (rad - limiarRad <= direcao[i][j] <= rad + limiarRad):
                magnitude[i][j] = 255
            else:
                magnitude[i][j] = 0
    #        print(direcao[i][j])
    #        break


#    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


#    cv2.imshow('Imagem PNG', magnitude)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#    np.savetxt('imagem_binaria.txt', imagem/255, fmt='%d')
#    print(imagem/255)


    return magnitude


