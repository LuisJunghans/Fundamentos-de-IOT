#Análise e Desenvolvimento de Sistemas - Caio Chacur Gobbi, Luis Felipe Bandeira Junghans e Mariana Crivelaro da Silva
#23/09/2023

import dht
import machine
import time
import urequests
import network

#criação dos dois objetos, d para o DHT11 e r para o Relé
d = dht.DHT11(machine.Pin(4))
r = machine.Pin(2, machine.Pin.OUT)

#função usada para medir a temperatura e a umidade do ambiente
def medicao():
    d.measure()
    print("Temperatura: {} graus  Umidade: {}%".format(d.temperature(), d.humidity()))

#função usada para acessar a rede wifi
def conecta(ssid, senha):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, senha)
        for t in range(50):
            if station.isconnected():
                break
            time.sleep(0.1)
        return station


#aqui é criado um loop para a conexão com o ThingSpeak e logo em seguida a medição da temperatura e o resultado para o acionamento ou nao do relé
while True:
    
    print("Conectando...")
    station = conecta("redewifi", "senha_redewifi") #local de alteração de rede e senha respectivamente
    if not station.isconnected():
        print("Nao conectado!...")
    else:
        print("Conectado!...")
        print("Acecssando o site...")
        response = urequests.get("https://api.thingspeak.com/update?api_key=DJAX1WRAFQ4A6BJ9&field1={}&field2={}".format(d.temperature(), d.humidity()))
        print("Pagina acessada: ")
        print(response.text)
        station.disconnect()
    time.sleep(5)
    
    medicao()
    temperatura = d.temperature()
    umidade = d.humidity()
    
    #condicionais para todos os casos possiveis
    #o loop será repetido caso nenhuma seja satisfeita
    #e caso seja satisfeita ela é executada e o loop retorna em seguida
    
    if temperatura > 31 and umidade > 70:
        print("A temperatura e a umidade estão muito altas!")
        r.value(1)
        time.sleep(2)
    elif temperatura > 31:
        print("A temperatura está muito alta!")
        r.value(1)
        time.sleep(2)
    elif umidade > 70:
        print("A umidade está muito alta!")
        r.value(1)
        time.sleep(2)
    else:    
        r.value(0)
        time.sleep(2)