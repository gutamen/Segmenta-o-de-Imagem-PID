import cv2
import numpy as np


def correcao(imagem, rad, limiarReconstrucao):
    altura, largura = imagem.shape[:2]
    if 1.5 <= rad[0] <= 1.6:
        for i in range(0, altura - 1):
            k = 0
            buraco = False
            comeco = True
            for j in range(0, largura - 1):       
                if imagem[i][j] > 0 and not buraco:
                    comeco = False
                elif imagem[i][j] == 0 and not comeco:
                    k += 1
                    buraco = True 
                    if k > limiarReconstrucao:
                        comeco = True
                        buraco = False
                        k = 0
                elif imagem[i][j] > 0 and buraco:
                    buraco = False
                    for l in range(k, 0, -1):
#                        print(str(i) + ' ' + str(j))
                        imagem[i][j - l] = 255
                    k = 0
                    comeco = True

                if buraco and j == largura - 1 and k > 0:
                    for l in range(k, 0, -1):
                        imagem[i][j - l] = 255
    return imagem

#   anguloSolicitado
#       1 = 0º
#       2 = 45º
#       3 = 90º
#       4 = 135º
#       5 = 180º
#       6 = Todos de 45º em 45º
def process(imagem, limiarMagnitude = 80, anguloSolicitado = 3, limiarAngular = 10, limiarReconstrucao = 10):
    grad_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)

    if anguloSolicitado == 1:
        anguloSolicitado = [0]
    elif anguloSolicitado == 2:
        anguloSolicitado = [45]
    elif anguloSolicitado == 3:
        anguloSolicitado = [90]
    elif anguloSolicitado == 4:
        anguloSolicitado = [135]
    elif anguloSolicitado == 5:
        anguloSolicitado = [180]
    elif anguloSolicitado == 6:
        anguloSolicitado = [0, 45, 90, 135, 180]
    else:
        print('Ângulo Solicitado inválido')
        return imagem


    # Valores
#    limiarMagnitude = 80    # entre 0 e 255
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
    
#    print(rad)
#    print(altura, largura)

#    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    for l in range(0, len(rad)):
        for i in range(0, altura - 1):
            for j in range(0, largura - 1):
                if magnitude[i][j] >= limiarMagnitude and (rad[l] - limiarRad <= direcao[i][j] <= rad[l] + limiarRad):
                    magnitude[i][j] = 255
    #                magnitude[i][j] = magnitude[i][j] 
                else:
                    magnitude[i][j] = 0
#                print(direcao[i][j])
        magnitude = correcao(magnitude, rad, limiarReconstrucao)
    
    return magnitude

    anguloRotacao = 45
    centro = (largura // 2, altura // 2)
    alturaRotacionada = int(largura * np.abs(np.sin(np.radians(anguloRotacao))) + altura * np.abs(np.cos(np.radians(anguloRotacao))))
    larguraRotacionada = int(altura * np.abs(np.sin(np.radians(anguloRotacao))) + largura * np.abs(np.cos(np.radians(anguloRotacao))))
    matrizRotacao = cv2.getRotationMatrix2D(centro, anguloRotacao, 1.0)
    matrizRotacao[0, 2] += (larguraRotacionada - largura) / 2
    matrizRotacao[1, 2] += (alturaRotacionada - altura) / 2

    centro = (larguraRotacionada // 2, alturaRotacionada // 2)
    magnitude = cv2.warpAffine(magnitude, matrizRotacao, (larguraRotacionada, alturaRotacionada), borderMode = cv2.BORDER_CONSTANT, borderValue = (0), flags=cv2.INTER_NEAREST)        
    print(magnitude.shape[:2])
    matrizRotacaoInversa = cv2.getRotationMatrix2D(centro, -anguloRotacao, 1.0)

    magnitude = cv2.warpAffine(magnitude, matrizRotacaoInversa, (larguraRotacionada, alturaRotacionada), flags=cv2.INTER_NEAREST)       
    
    mid_x, mid_y = int(larguraRotacionada/2), int(alturaRotacionada/2)
    cw2, ch2 = int(largura/2), int(altura/2)

    return magnitude[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
#    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


#    cv2.imshow('Imagem PNG', magnitude)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#    np.savetxt('imagem_binaria.txt', imagem/255, fmt='%d')
#    print(imagem/255)

    
