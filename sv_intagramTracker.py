import socket
import sys
import threading
import urllib
import unicodedata
from bs4 import BeautifulSoup

#Creando el socket TCP/IP (Coneccion TCP a IP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind() es para asociar un socket a una direccion de servidor.
server_address = ('192.168.1.46', 8800)
print (sys.stderr, 'Empezando a levantar "%s" puerto "%s"' % server_address)
sock.bind(server_address)
print("Punto control 1 : ")

#El metodo accept() acepta conexion entrante (un cliente)
#EL metodo listen() pone al socket en modo servidor

#Escuchando conexion
sock.listen(1)



def worker(*args):
    conn = args[0]
    addr = args[1]
    
    url = conn.recv(500)

    print('Buscando la direccion  %s' % url.decode("utf8"))
    print("Se a conectado un usuario!")
  


#método de análisis de una dirección web
def analisisDescarga(archivo,conexion):
    html = conexion.read()
    soup = BeautifulSoup(html)
    #obtenemos una lista de String con la condición de atributos class con valores details y price
    links = soup.find_all(True, {'class':['.g47SY']})
    #la lista alterna valores de nombre de producto y precio
    #   creamos una bandera para diferenciar si es valor o producto
    precio = False
    for tag in links:
        print("--")
        for linea in tag:
            linea = linea.strip()
            #adaptamos unicode a utf-8
            normalizado=unicodedata.normalize('NFKD', linea).encode('ascii','ignore')
            if len(normalizado)>1:
                if precio:
                    print('precio: '+normalizado)
                    precio= not precio
                    archivo.write(normalizado+'\n')
                else:
                    print('producto: '+normalizado)
#este método se conectará con la web y establece un timeout que obliga a reintentar el fallo
def preparar(archivo,web,x):
    try:
        print(web)
        conector = urllib2.urlopen(web,timeout=10)#timeout de 10 segundos
        analisisDescarga(archivo,conector)
    except:
        print("Tiempo de espera agotado, volviendo a intentar")
        preparar(archivo,web,x)
 



for x in range(0,177):
    #Ruta de la página web
    url = 'http://www.dia.es/compra-online/productos/c/WEB.000.000.00000?q=%3Aname-asc&page='+str(x)+'&disp=grid'
    preparar(archivo,url,x)
 


while True:
    conn, addr = sock.accept()
    threading.Thread(target=worker, args=(conn, addr)).start()
worker()


 