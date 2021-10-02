import cv2
import os, sys, os.path
import numpy as np

#filtro baixo
image_lower_hsv1 = np.array([0, 165, 89])
image_upper_hsv1 = np.array([0, 255, 255])

#filtro alto
image_lower_hsv2 = np.array([0, 130, 190])
image_upper_hsv2 = np.array([97, 255, 255])


def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask


def mascara_or(mask1, mask2):
    """ retorna a mascara or"""
    mask = cv2.bitwise_or(mask1, mask2)
    return mask


def mascara_and(mask1, mask2):
    """ retorna a mascara and"""
    mask = cv2.bitwise_and(mask1, mask2)
    return mask


def dsn_cruz(img, cX, cY, size, color):
    """ faz a cruz no ponto cx cy"""
    cv2.line(img, (cX - size, cY), (cX + size, cY), color, 5)
    cv2.line(img, (cX, cY - size), (cX, cY + size), color, 5)


def esv_txt(img, text, org, color):
    """ faz a cruz no ponto cx cy"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(text), org, font, 1, color, 2, cv2.LINE_AA)

def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """
    mask_hsv1 = filtro_de_cor(img, image_lower_hsv1, image_upper_hsv1)
    mask_hsv2 = filtro_de_cor(img, image_lower_hsv2, image_upper_hsv2)

    mask_hsv = mascara_or(mask_hsv1, mask_hsv2)

    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB)
    contor_img = mask_rgb.copy()

    b1 = None
    b2 = None
    b3 = None
    b4 = None

    lista = []


    for c in contornos:
        area = int(cv2.contourArea(c))
        lista.append(area)
    lista.sort(reverse=True)

    print(lista)

    for d in contornos:
        area = int(cv2.contourArea(d))
        if lista[0] == area:
            b1 = d
        elif lista[1] == area:
            b2 = d
        elif lista[2] == area:
            b3 = d
        elif lista[3] == area:
            b4 = d
            

    M1 = cv2.moments(b1)
    M2 = cv2.moments(b2)
    M3 = cv2.moments(b3)
    M4 = cv2.moments(b4)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if M1["m00"] != 0 and M2["m00"] != 0 and M3["m00"] and M4["m00"]:
        cX1 = int(M1["m10"] / M1["m00"])
        cY1 = int(M1["m01"] / M1["m00"])
        cX2 = int(M2["m10"] / M2["m00"])
        cY2 = int(M2["m01"] / M2["m00"])

        cv2.drawContours(contor_img, [b1], -1, [11, 11, 117], thickness=cv2.FILLED)
        cv2.drawContours(contor_img, [b2], -1, [208, 226, 79], thickness=cv2.FILLED)
        cv2.drawContours(contor_img, [b3], -1, [0, 0, 0], thickness=cv2.FILLED)
        cv2.drawContours(contor_img, [b4], -1, [0, 0, 0], thickness=cv2.FILLED)
    
        #faz a cruz no centro de massa
        dsn_cruz(contor_img, cX1, cY1, 20, (11, 11, 177))
        dsn_cruz(contor_img, cX2, cY2, 20, (208, 226, 79))

        # Para escrever vamos definir uma fonte
        txt1 = cY1, cX1
        org1 = (cY1+80, cX1-150)

        txt2 = cY2, cX2
        org2 = (cY2+80, cX2-150)

        esv_txt(contor_img, txt1, org1, (11, 11, 177))
        esv_txt(contor_img, txt2, org2, (208, 226, 79))

        coord1 = (cX1, cY1)
        coord2 = (cX2, cY2)
        cv2.line(contor_img, coord1, coord2, (0, 255, 0), 4)

    else:
    # se não existe nada para segmentar
        cX1, cY2 = 0, 0
        texto = 'nao tem nada'
        org = (0, 50)
        esv_txt(contor_img, texto, org, (0, 0, 255))

    return contor_img


cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

# vc = cv2.VideoCapture("teste.mp4") # para ler um video mp4

#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened():  
    rval, frame = vc.read()
else:
    rval = False

while rval:

    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
