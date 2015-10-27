#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_clientes = {}

    def get_nombre(self, mensaje):
        nombre = mensaje.split(" ")[1]
        nombre = nombre.split(":")[1]
        return nombre


    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        dir_client = self.client_address[0]
        port_client = self.client_address[1]

        line = self.rfile.read()

        #si es REGISTER debemos guardar el cliente
        mensaje_recibido = line.decode('utf-8')
        tipo_mensaje = mensaje_recibido.split(' ')[0]
        if tipo_mensaje == "REGISTER":
            print("El cliente nos manda " + tipo_mensaje)
            #guardo al cliente
            nombre = self.get_nombre(mensaje_recibido)
            self.dicc_clientes[nombre] = dir_client
            #traza
            print(self.dicc_clientes)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")


        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            mensaje_recibido = line.decode('utf-8')
            print("El cliente nos manda " + mensaje_recibido)

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
