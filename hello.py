import cv2
import base64
import numpy as np
import controller as cnt
from cvzone.HandTrackingModule import HandDetector

# Inicializando o detector de mãos
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Inicializando a captura de vídeo
video = cv2.VideoCapture(0)

# Inicializando o estado
estado = "Inativo"

# Base64 de uma imagem (substitua com a sua imagem base64)
img_base64 = "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"
# Decodificando a imagem base64
img_data = base64.b64decode(img_base64)
img_array = np.frombuffer(img_data, dtype=np.uint8)
logo = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

# Redimensionar o logo se necessário
logo = cv2.resize(logo, (100, 100))

# Criando uma janela em tela cheia
cv2.namedWindow("Robótica Aplicada - Aula ITE", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Robótica Aplicada - Aula ITE", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
        # Capturando um frame do vídeo
    # Capturando um frame do vídeo
    ret, frame = video.read()

    # Espelhando o frame horizontalmente
    frame = cv2.flip(frame, 1)

    # Obtendo as dimensões do frame
    altura, largura, _ = frame.shape

    # Detectando mãos no frame
    hands, img = detector.findHands(frame)

    if hands:
        # Atualizando o estado para ativo
        estado = "Ativo"
        cor = (0, 255, 0)  # Verde

        # Obtendo a lista de pontos de referência da mão
        lmList = hands[0]

        # Obtendo os dedos levantados
        fingerUp = detector.fingersUp(lmList)

        # Ativando os LEDs com base nos dedos levantados
        cnt.led(fingerUp)

        # Contando o número total de dedos levantados
        total_fingers = sum(fingerUp)

        # Exibindo a contagem de dedos levantados no canto inferior esquerdo da tela
        cv2.putText(frame, f'Dedos Levantados: {sum(fingerUp)}', (20, altura - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Exibindo o array de dedos levantados no canto inferior direito da tela
        cv2.putText(frame, f'Dedos Levantados Array: {str(fingerUp)}', (largura - 360, altura - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        
    else:
        # Atualizando o estado para inativo
        estado = "Inativo"
        cor = (0, 0, 255)  # Vermelho

    # Definindo a posição para o texto
    altura, largura, _ = frame.shape
    posicao_texto = (largura - 200, 50)

    # Adicionando fundo semi-transparente para o texto do estado e "ITE"
    overlay = frame.copy()
    cv2.rectangle(overlay, (posicao_texto[0] - 10, posicao_texto[1] - 30), (largura - 10, posicao_texto[1] + 80), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    # Exibindo o estado atual e a inscrição "ITE" na tela com sombra
    cv2.putText(frame, f'{estado}', posicao_texto, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)  # Sombra
    cv2.putText(frame, f'{estado}', posicao_texto, cv2.FONT_HERSHEY_COMPLEX, 1, cor, 2, cv2.LINE_AA)
    cv2.putText(frame, 'ITE', (posicao_texto[0], posicao_texto[1] + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)  # Sombra
    cv2.putText(frame, 'ITE', (posicao_texto[0], posicao_texto[1] + 50), cv2.FONT_HERSHEY_COMPLEX, 1, cor, 2, cv2.LINE_AA)

    # Adicionando logotipo/ícone
    if logo is not None:
        # Pegando as dimensões do logo
        logo_height, logo_width = logo.shape[:2]
        # Posicionando o logo no canto superior esquerdo
        frame[10:10 + logo_height, 10:10 + logo_width] = logo

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
