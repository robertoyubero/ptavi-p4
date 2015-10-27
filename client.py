#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

def to_register(mensaje, my_direction):
    salida = "REGISTER "
    salida = salida + "sip:"+ my_direction + " SIP/2.0\r\n\r\n" + mensaje
    print("Enviando: " + "REGISTER")
    return salida

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
tipo_mensaje = sys.argv[3]
my_dir = sys.argv[4]

# Contenido que vamos a enviar
LINE = sys.argv[3:]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

frase = ' '.join(LINE)



#enviamos mensaje REGISTER
my_socket.send(bytes(to_register(frase, my_dir), 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
