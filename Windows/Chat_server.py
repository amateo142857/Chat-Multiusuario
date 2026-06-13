## Chat multiusuario ##
# Servidor
#!/usr/bin/env python3

import tkinter as tk
import socket
import threading
import ssl
import signal
import sys

# Variable global para controlar la ejecución
ejecutando = True

def signal_handler(sig, frame):
    """ Maneja la señal de Ctrl+C """
    global ejecutando
    print("\n[!] Recibida señal de interrupción. Cerrando servidor...")
    ejecutando = False
    sys.exit(0)

def hilos_cliente(socket_cliente, clientes, usuarios):
    nombre_usuario = socket_cliente.recv(1024).decode()
    usuarios[socket_cliente] = nombre_usuario
    print(f"[+] El usuario {nombre_usuario} se ha conectado")
    
    try:
        for cliente in clientes:
            if cliente is not socket_cliente:
                try:
                    cliente.sendall(f"\n[+] El usuario {nombre_usuario} ha entrado al chat\n\n".encode())
                except:
                    pass
        
        while ejecutando:
            try:
                # Establecer timeout para poder verificar ejecutando periódicamente
                socket_cliente.settimeout(1.0)
                mensaje = socket_cliente.recv(1024).decode()
                socket_cliente.settimeout(None)
                
                if not mensaje:
                    break
                    
                if "!usuarios" in mensaje.strip():
                    socket_cliente.sendall(f"\n[+] Listado de usuarios disponibles: {', '.join(usuarios.values())} \n\n".encode())
                    continue
                
                for cliente in clientes:
                    if cliente is not socket_cliente:
                        try:
                            cliente.sendall(f"{mensaje}\n".encode())
                        except:
                            pass
            except socket.timeout:
                # Timeout, continuar para verificar ejecutando
                continue
            except:
                break
    except:
        pass
    finally:
        # Limpiar recursos del cliente
        try:
            socket_cliente.close()
        except:
            pass
        
        if socket_cliente in clientes:
            clientes.remove(socket_cliente)
        if socket_cliente in usuarios:
            del usuarios[socket_cliente]
        print(f"[-] El usuario {nombre_usuario} se ha desconectado")

def cerrar_servidor(socket_servidor, clientes, usuarios):
    """Cierra el servidor y todas las conexiones de clientes"""
    global ejecutando
    print("\n[+] Cerrando servidor...")
    ejecutando = False
    
    # Notificar a todos los clientes
    for cliente in clientes:
        try:
            cliente.sendall("\n[!] El servidor se está cerrando. Conexión terminada.\n".encode())
            cliente.close()
        except:
            pass
    
    # Cerrar socket del servidor
    try:
        socket_servidor.close()
    except:
        pass
    
    print("[+] Servidor cerrado correctamente")
    sys.exit(0)
    
def Servidor():
    global ejecutando
    
    host = '192.168.1.2'
    port = 12345
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    # Crear el socket normal
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        socket_servidor.bind((host, port))
    except Exception as e:
        print(f"[!] Error al bindear el puerto {port}: {e}")
        return
    
#    # Crear contexto SSL
#    try:
#        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#        context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.key")
#        # Envolver el socket con SSL
#        socket_servidor = context.wrap_socket(socket_servidor, server_side=True)
#    except Exception as e:
#        print(f"[!] Error al configurar SSL: {e}")
#        print("[!] Asegúrate de que los archivos server-cert.pem y server-key.key existen")
#        return
    
    socket_servidor.listen()
    socket_servidor.settimeout(1.0)  # Timeout para poder verificar ejecutando
    
    print(f"[+] El servidor está en escucha de conexiones entrantes en {host}:{port}")
    print("[+] Presiona Ctrl+C para cerrar el servidor")
    
    clientes = []
    usuarios = {} 
    
    try:
        while ejecutando:
            try:
                socket_cliente, address = socket_servidor.accept()
                clientes.append(socket_cliente)
                print(f"[+] Se ha conectado un nuevo cliente: {address}")
                
                thread = threading.Thread(target=hilos_cliente, args=(socket_cliente, clientes, usuarios))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                # Timeout normal, continuar para verificar ejecutando
                continue
            except OSError as e:
                if ejecutando:
                    print(f"[!] Error en accept: {e}")
                break
    except KeyboardInterrupt:
        print("\n[!] Interrupción manual detectada")
    finally:
        cerrar_servidor(socket_servidor, clientes, usuarios)
    
if __name__ == '__main__':
    try:
        Servidor()
    except KeyboardInterrupt:
        print("\n[!] Servidor terminado por el usuario")
        sys.exit(0)
