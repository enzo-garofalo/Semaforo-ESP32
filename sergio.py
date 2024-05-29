#import network
#import time
#from micropyserver import MicroPyServer

#sta = network.WLAN(network.STA_IF)
#sta.active(False)
#sta.active(True)

#redes = sta.scan()
#print(f'redes = {redes}')
#sta.active(False)

#for rede in redes:
    #print(rede)

###########################################
import network
from time import sleep
from machine import Pin, PWM
from micropyserver import MicroPyServer
import time 
import json

# Configuração dos pinos do motor direito
led_vermelho = Pin(4, Pin.OUT)
led_amarelo = Pin(0, Pin.OUT)
led_verde = Pin(16, Pin.OUT)

ssid = 'PUC-ACD'
password =''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)


while not station.isconnected():
    print(".",end="")
    time.sleep(0.1)

print('Conectado à rede', ssid)
print('Configuração de rede:', station.ifconfig())

server = MicroPyServer()
# Página HTML para controle
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Botões de Controle</title>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f0f0f0;
      margin: 0;
    }
    .frame {
      text-align: center;
      background-color: white;
      padding: 50px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .button {
      display: block;
      width: 100px;
      margin: 10px auto;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    .red { background-color: #ff4d4d; }
    .green { background-color: #4dff4d; }
    .yellow { background-color: #ffff4d; }
    .off { background-color: #d9d9d9; }
  </style>
</head>
<body>
  <div class="frame">
    <button class="button red" onclick="callEndpoint('/red')">Red</button>
    <button class="button yellow" onclick="callEndpoint('/yellow')">yellow</button>
    <button class="button green" onclick="callEndpoint('/green')">green</button>
  </div>

  <script>
    function callEndpoint(endpoint) {
      const url = `${endpoint}`;
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  </script>
</body>
</html>
"""
def inicio(request):
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: text/html\r\n\r\n")
    server.send(html)


def red(request):
    led_vermelho.value(not led_vermelho.value())            
    json_str = json.dumps({"status": "ok"})
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: application/json\r\n\r\n")
    server.send(json_str)
    
def yellow(request):
    led_amarelo.value(not led_amarelo.value())            
    json_str = json.dumps({"status": "ok"})
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: application/json\r\n\r\n")
    server.send(json_str)

def green(request):
    led_verde.value(not led_verde.value())            
    json_str = json.dumps({"status": "ok"})
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: application/json\r\n\r\n")
    server.send(json_str)



server.add_route('/', inicio)
server.add_route('/red', red)
server.add_route('/yellow', yellow)
server.add_route('/green', green)

server.start()

