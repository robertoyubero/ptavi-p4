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
    dicc_clientes = {}

    def json2registered(self):
        """
        Extraigo la informacion de mis clientes de un fichero json
        """
        try:
            fichero = open('registered.json')
            print("True >> el fichero existe")
            content = json.load(fichero)
            print(len(content))
            print("--------------------------")
        except FileNotFoundError:
            print("False >> el fichero no existe")

    def registered2json(self,nombre, dir_maquina, t_exp):
        """
        Guardo mis clientes en un fichero json
        """
        dicc = {}
        dicc['adress'] = dir_maquina
        dicc['expires'] = t_exp
        contenido = [nombre, dicc]

        #guardo informacion del cliente
        fichero = open('registered.json', 'a')
        #guardo el fichero
        json.dump(contenido, fichero)
        fichero.close()
        """---------------------------------"""
        #imprimo informacion del cliente desde el fichero .json
        fichero = open('registered.json', 'r')
        #copio el contenido del fichero json
        contenido = fichero.readlines()
        #imrpimo del fichero .json el ultimo cliente
        print(contenido[0][-75:])


    def get_time_expiration(self, t_expiracion):
        """
        Calculo cuando expirará mi sesión
        """
        #le sumo una hora a la hora actual
        hora_expiracion = time.time() + 3600
        #le sumo el t_expiracion a la hora
        hora_expiracion += t_expiracion
        hora_expiracion = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(hora_expiracion))
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

            #imprimimos fichero con register2json
            self.registered2json(nombre, local_host, hora_expiracion)
            #compruebo si debo borrar o no
            if t_expires == 0:
                try:
                    del self.dicc_clientes[nombre];
                    print("usuario eliminado de mis diccionario de clientes")

                except:
                    print("no tengo guardado el usuario, no hago nada")
            else:
                #guardo al usuario
                self.dicc_clientes[nombre] = dir_cliente

            #respondo al cliente
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
