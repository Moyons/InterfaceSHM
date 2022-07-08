import socket
import time
import os
import shutil

HOST = "192.168.10.60"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Aquí creamos un objeto socket
s = socket.socket()
s.bind((HOST, PORT))
print("El socket se pone en modo para escuchar.")
s.listen(1)
print("El socket espera una conexión entrante.")
conn, addr = s.accept()

path = 'files'

while True:
    data = conn.recv(1024)
    datosRecibidos = data.decode()
    print("Datos recibidos: " + datosRecibidos)

    if datosRecibidos == "EXIT":
        conn.send(data)
        print("Se sale de la aplicación")
        break
    elif datosRecibidos[0] == "1":
        print("Ejecuta un Simple Test")
        fileExists = os.path.exists(path)
        if fileExists:
            shutil.rmtree(path)
        else:
            os.mkdir(path)
        command = "./main binary_container_1.xclbin " + datosRecibidos
        if os.system(command) == 0:
            print("Ha terminado la ejecución del Simple Test")
        result = "Finish"
        conn.send(result.encode())
    elif datosRecibidos[0] == "2":
        print("Ejecuta un Round Robin")
        fileExists = os.path.exists(path)
        if fileExists:
            shutil.rmtree(path)
        else:
            os.mkdir(path)
        command = "./main binary_container_1.xclbin " + datosRecibidos
        if os.system(command) == 0:
            print("Ha terminado la ejecución del Round Robin")
        result = "Finish"
        conn.send(result.encode())
    elif datosRecibidos[0] == "3":
        print("Ejecuta un Passive Test")
        fileExists = os.path.exists(path)
        if fileExists:
            shutil.rmtree(path)
        else:
            os.mkdir(path)
        command = "./main binary_container_1.xclbin " + datosRecibidos
        if os.system(command) == 0:
            print("Ha terminado la ejecución del Passive Test")
        result = "Finish"
        conn.send(result.encode())
    elif datosRecibidos[0] == "4":
        print("Ejecuta un Impact Detected")
        fileExists = os.path.exists(path)
        if fileExists:
            shutil.rmtree(path)
        else:
            os.mkdir(path)
        command = "./main binary_container_1.xclbin " + datosRecibidos
        if os.system(command) == 0:
            print("Ha terminado la ejecución del Impact Detected")
        result = "Finish"
        conn.send(result.encode())
    else:
        conn.send(data)


conn.close()
s.close()
