#Análise e Desenvolvimento de Sistemas - Caio Chacur Gobbi, Luis Felipe Bandeira Junghans e Mariana Crivelaro da Silva
#23/09/2023

import urequests
import network
import time

#inicio de um loop que conecta o esp32 à rede wifi
while True:
    def conecta(ssid, senha):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, senha)
        for t in range(50):
            if station.isconnected():
                break
            time.sleep(0.1)
        return station


    print("Conectando...")
    station = conecta("redewifi", "senha_redewifi")
    if not station.isconnected():
        print("Nao conectado!...")
    else:
        print("Conectado!...")
        print("Acecssando o site...")
        response = urequests.get("https://api.thingspeak.com/update?api_key=DJAX1WRAFQ4A6BJ9&field1=0&field2=0")
        print("Pagina acessada: ")
        print(response.text)
        station.disconnect()