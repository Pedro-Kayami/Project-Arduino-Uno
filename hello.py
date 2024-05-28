import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector

# Inicializando o detector de mãos
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Inicializando a captura de vídeo
video = cv2.VideoCapture(0)

while True:
    # Capturando um frame do vídeo
    ret, frame = video.read()

    # Espelhando o frame horizontalmente
    frame = cv2.flip(frame, 1)

    # Detectando mãos no frame
    hands, img = detector.findHands(frame)

    if hands:
        # Obtendo a lista de pontos de referência da mão
        lmList = hands[0]

        # Obtendo os dedos levantados
        fingerUp = detector.fingersUp(lmList)
        

        # Ativando os LEDs com base nos dedos levantados
        cnt.led(fingerUp)

        # Contando o número total de dedos levantados
        total_fingers = sum(fingerUp)

        # Exibindo o número total de dedos levantados na tela
        cv2.putText(frame, f'Dedos Totais: {total_fingers}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # Exibindo o frame na janela
    cv2.imshow("Robótica Aplicada - Aula ITE", frame)

    # Aguardando o pressionamento de uma tecla
    k = cv2.waitKey(1)

    # Verificando se a tecla 'k' foi pressionada para sair do loop
    if k == ord("k"):
        break

# Liberando a captura de vídeo e fechando todas as janelas
video.release()
cv2.destroyAllWindows()
