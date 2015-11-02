#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_json = {}

    def json2registered(self):
        """
        Extraigo la informacion de mis clientes de un fichero json
        """
        try:
            fichero = open('registered.json')
            contenido = json.load(fichero)
            a = int(len(contenido)/2)

            for i in range(0, a):
                for x in contenido.keys():
                    #guardo cliente mas contenido
                    self.dicc_json[x] = contenido[x]
        except FileNotFoundError:
            pass

    def registered2json(self, usuario):
        """
        Guardo mis clientes en un fichero json
        """
        #leo el fichero que tenia guardado
        try:
            fichero = open('registered.json', 'w')
            json.dump(self.dicc_json, fichero)
            fichero.close()

        except FileNotFoundError:
            fichero = open('registered.json', 'w')
            json.dump(self.dicc_json, fichero)
            fichero.close()

        """---------------------------------"""
        #imprimo informacion del cliente desde el fichero .json
        fichero = open('registered.json', 'r')
        #copio el contenido del fichero json
        contenido = json.load(fichero)
        #imrpimo del fichero .json el ultimo cliente
        esta = usuario in contenido.keys()
        if esta:
            print("\nRECIBIDO REGISTER DE: ")
            print(usuario + " ," + str(contenido[usuario]))

    def get_time_expiration(self, t_expiracion):
        """
        Calculo cuando expirará mi sesión
        """
        #le sumo una hora a la hora actual
        hora_expiracion = time.time() + 3600
        #le sumo el t_expiracion a la hora
        hora_expiracion += t_expiracion
        hora_expiracion = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(hora_expiracion))
        return hora_expiracion

    def get_nombre(self, mensaje):
        """
        Extraigo el nombre del usuario del mensaje
        """
        nombre = mensaje.split(" ")[1]
        nombre = nombre.split(":")[1]
        return nombre

    def get_expires(self, mensaje):
        """
        Extraigo el tiempo de expiracion del mensaje
        """
        time = mensaje.split("Expires: ")[1]
        time = time.split("\r")[0]
        return(int(time))

    def handle(self):

        while 1:

            # Escribe dirección y puerto del cliente (de tupla client_address)
            dir_cliente = self.client_address[0]
            port_cliente = self.client_address[1]
            local_host = str(dir_cliente) + " " + str(port_cliente)
            line = self.rfile.read()
            mensaje_recibido = line.decode('utf-8')
            tipo_mensaje = mensaje_recibido.split(' ')[0]

            """-----------
            -----REGISTER
            ------------"""
            if tipo_mensaje == "REGISTER":
                nombre = self.get_nombre(mensaje_recibido)
                t_expires = self.get_expires(mensaje_recibido)
                hora_expiracion = self.get_time_expiration(t_expires)

                #comprobamos si existe fichero
                self.json2registered()
                #compruebo si debo borrar o no
                if t_expires == 0:
                    if nombre in self.dicc_json:
                        #elimino el usuario del diccionario
                        del self.dicc_json[nombre]
                        self.registered2json(nombre)
                        print("\n" + nombre + " SE HA DESCONECTADO")
                else:
                    #guardo al usuario
                    dir_maquina = dir_cliente + " " + str(port_cliente)
                    dicc = {}
                    dicc['adress'] = dir_maquina
                    dicc['expires'] = hora_expiracion
                    self.dicc_json[nombre] = dicc
                    self.registered2json(nombre)
                    #respondo al cliente
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
