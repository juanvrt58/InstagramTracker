import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.1.46', 8800)

print ("Conectando a %s con el puerto %s" % server_address)
sock.connect(server_address)

def buscar_url(url_input):
    url_input = input("Ingresa la url del perfil de instagram : ")
    return url_input
    
url = buscar_url(url_input = "")

sock.sendto(url.encode(), server_address)
