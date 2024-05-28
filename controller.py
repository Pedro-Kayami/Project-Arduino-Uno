import pyfirmata
import requests
import json
import time
import sys

comport = 'COM5'

board = pyfirmata.Arduino(comport)

led_1 = board.get_pin('d:7:o')
led_2 = board.get_pin('d:8:o')
led_3 = board.get_pin('d:9:o')
led_4 = board.get_pin('d:10:o')
led_5 = board.get_pin('d:11:o')
led_6 = board.get_pin('d:12:o')
led_7 = board.get_pin('d:13:o')

# Definindo um atraso de 10 segundos entre as mensagens
DELAY_SECONDS = 10

# Último tempo em que uma mensagem foi enviada
last_message_time = 0

# Estado anterior dos LEDs
previous_led_state = [1, 1, 1, 1, 1, 1, 1]

def send_discord_message(message):
    # Substitua 'SEU_WEBHOOK_URL_AQUI' pela URL do seu webhook do Discord
    discord_webhook_url = 'https://discord.com/api/webhooks/1245114684450017281/2fKRNn-E7HPZJB5gUcEq0AhIsQxcXaLMbNGMAmC_0zTYfsPKdyZnCvcmu9aeTA3tryCp'
    if discord_webhook_url:
        payload = {
            "content": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(discord_webhook_url, data=json.dumps(payload), headers=headers)
            if response.status_code != 200:
                print(f"Erro ao enviar mensagem para o Discord: {response.text}")
        except Exception as e:
            print(f"Erro ao tentar enviar mensagem para o Discord: {e}")

def led(fingerUp):
    global last_message_time, previous_led_state

    current_time = time.time()

    # Verificando se todos os LEDs foram apagados
    all_leds_off = all(led == 0 for led in fingerUp)

    # Verificando se todos os LEDs foram acesos
    all_leds_on = all(led == 1 for led in fingerUp)

    # Verificando se a mão acendeu ou apagou todos os LEDs
    if (all_leds_off or all_leds_on) and current_time - last_message_time >= DELAY_SECONDS:
        last_message_time = current_time

        # Verificando se todos os LEDs foram apagados
        if all_leds_off:
            message = "# Alteração LED #\n> Todos os LEDs foram apagados!"
        else:
            message = "# Alteração LED #\n> Todos os LEDs foram acesos!"
        
        send_discord_message(message)

    # Atualizando o estado anterior dos LEDs
    previous_led_state = fingerUp

    # Log da posição dos dedos
    print(f"Posição atual dos dedos: {fingerUp}")

    # Restante do código para acender as luzes
    if fingerUp == [0, 0, 0, 0, 0]:
        leds = [led_1, led_2, led_3, led_4, led_5, led_6, led_7]
        for led_pin in leds:
            led_pin.write(0)
    # Se alguma luz estiver ligada, envie uma mensagem apenas se o intervalo de atraso for atendido
    elif any(fingerUp) and current_time - last_message_time >= DELAY_SECONDS:
        last_message_time = current_time
        led_status = "ligada" if any(fingerUp) else "desligada"
        message = f"# Alteração LED #\n> Agora a luz está {led_status}!"
        send_discord_message(message)

    # Restante do código para acender as luzes
    if fingerUp == [0,0,0,0,0]:
        led_1.write(0)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)
        led_6.write(0)
        led_7.write(0)
    elif fingerUp == [0,0,0,0,1]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(1)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [0,1,1,0,0]:
        led_1.write(1)#Corredor
        led_2.write(1)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça  
    elif fingerUp == [0,1,1,1,0]:
        led_1.write(1)#Corredor
        led_2.write(1)#Quarto de solteiro
        led_3.write(1)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [0,1,1,1,1]:
        led_1.write(1)#Corredor
        led_2.write(1)#Quarto de solteiro
        led_3.write(1)#Cozinha
        led_4.write(1)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [1,1,1,1,1]:
        led_1.write(1)#Corredor
        led_2.write(1)#Quarto de solteiro
        led_3.write(1)#Cozinha
        led_4.write(1)#Sala
        led_5.write(1)#Sala de jantar
        led_6.write(1)#Banheiro
        led_7.write(1)#Quarto da bagunça
    elif fingerUp == [1,0,1,1,1]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(1)#Quarto da bagunça
    elif fingerUp == [0,1,0,0,1]:
        led_1.write(0)#Corredor
        led_2.write(1)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [0,0,0,1,1]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(1)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [1,0,0,0,1]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(1)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [1,0,0,0,0]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(1)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [0,1,0,0,0]:
        led_1.write(1)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
    elif fingerUp == [1,0,1,0,0]:
        led_1.write(0)#Corredor
        led_2.write(0)#Quarto de solteiro
        led_3.write(0)#Cozinha
        led_4.write(0)#Sala
        led_5.write(0)#Sala de jantar
        led_6.write(0)#Banheiro
        led_7.write(0)#Quarto da bagunça
        print("Última condição atendida, encerrando o programa.")
        sys.exit()

# Exemplo de uso:
# led([1, 0, 0, 0, 0])  # Isso irá acender a primeira luz
