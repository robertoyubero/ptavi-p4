#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


def to_register(my_direction, time_expiration):
    salida = "REGISTER "
    salida = salida + "sip:" + my_direction + " SIP/2.0\r\n"
    salida = salida + "Expires: " + time_expiration + "\r\n\r\n"
    print("Enviando: " + "REGISTER + expires")
    return salida

# Cliente UDP simple.
try:
    # Dirección IP del servidor.
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    tipo_mensaje = sys.argv[3]
    my_dir = sys.argv[4]
    t_expires = sys.argv[5]
    if int(t_expires) < 0:
        print("Solo tiempos de expiracion => 0. DEBO LANZAR EXCEPCION!!!")

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    #enviamos mensaje REGISTER
    my_socket.send(bytes(to_register(my_dir, t_expires), 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

    # Cerramos todo
    my_socket.close()
    print("Fin.")

except IndexError:
    print("Usage: client.py ip puerto register sip_address expires_value")
