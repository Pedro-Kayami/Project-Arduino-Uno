import cv2
from cvzone.HandTrackingModule import HandDetector

# Configuração do detector de mãos para detectar até duas mãos
detector = HandDetector(detectionCon=0.8, maxHands=2)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)  # Inverte a imagem da câmera horizontalmente
    hands, img = detector.findHands(frame)
    
    if hands:
        # Inverte a ordem das mãos detectadas
        hands = hands[::-1]
        
        for hand in hands:
            lmList = hand['lmList']
            fingerUp = detector.fingersUp(hand)
            print(fingerUp)

            # Posição da mão para exibição de texto
            x, y, w, h = hand['bbox']
            cv2.putText(frame, f'Fingers: {fingerUp}', (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255, 255, 255), 1, cv2.LINE_AA)

    # Adiciona o texto "ITE" no canto superior esquerdo da tela
    cv2.putText(frame, 'ITE', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
