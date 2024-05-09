import PIL
import cv2
import numpy as np
from bordasLocais import bordasLocais

imagem = cv2.imread('tijolo.png', cv2.IMREAD_GRAYSCALE)
imagem = bordasLocais(imagem)
#imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
#imagem = cv2.GaussianBlur(imagem, (5, 5), 0)
#_, imagem = cv2.threshold(imagem, 127, 255, cv2.THRESH_BINARY)


cv2.imshow('Imagem PNG', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()




