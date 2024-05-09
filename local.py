import cv2
import numpy as np

#   anguloSolicitado
#       1 = 0º
#       2 = 45º
#       3 = 90º
#       4 = 135º
#       5 = 180º

def process(imagem, limiarMagnitude = 80, anguloSolicitado = 1, limiarAngular = 10, limiarReconstrucao = 10):
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
    
#    print(len(rad))

#    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    for i in range(0, altura - 1):
        for j in range(0, largura - 1):
            if magnitude[i][j] >= limiarMagnitude and ((rad - limiarRad <= direcao[i][j]).any() and (direcao[i][j] <= rad + limiarRad).any()):
                magnitude[i][j] = 255
#                magnitude[i][j] = magnitude[i][j] 
            else:
                magnitude[i][j] = 0
#            print(direcao[i][j])
    
    if len(rad) == 1:
        if rad[0] == 1:
            k = 0
            buraco = False
            comeco = True
            for i in range(0, altura - 1):
                for j in range(0, largura - 1):       
                    if magnitude[i][j] > 0 and not buraco:
                        comeco = False
                    elif magnitude[i][j] == 0 and not comeco:
                        k += 1
                        buraco = True 
                        if k + 1 > limiarReconstrucao:
                            comeco = True
                            buraco = False
                            k = 0
                    elif magnitude[i][j] > 0 and buraco:
                        buraco = False
                        
                        




#    magnitude_normalizada = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


#    cv2.imshow('Imagem PNG', magnitude)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#    np.savetxt('imagem_binaria.txt', imagem/255, fmt='%d')
#    print(imagem/255)


    return magnitude


