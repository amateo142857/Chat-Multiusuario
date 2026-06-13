## Chat multiusuario ##
# Servidor #
#!/usr/bin/env python3

import tkinter as tk
import socket
import threading
import ssl
import signal
import sys

# Variable global para controlar la ejecución
ejecutando = True


def comprobar_credenciales(usuario, contrasena):
    """
    Verifica si las credenciales existen en el archivo password.txt
    """
    # Validar que los parámetros no estén vacíos
    if not usuario or not contrasena:
        print("[!] Usuario y contraseña no pueden estar vacíos")
        return False
    
    try:
        with open('password/password.txt', 'r', encoding='utf-8') as archivo:
            for num_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                
                # Saltar líneas vacías o comentarios
                if not linea or linea.startswith('#'):
                    continue
                
                # Separar usuario y contraseña (soporta múltiples espacios)
                partes = linea.split()
                
                if len(partes) >= 2:
                    user = partes[0]
                    pwd = partes[1]
                    
                    # Comparación exacta (incluyendo mayúsculas/minúsculas para usuario)
                    # Para contraseña es sensible a mayúsculas/minúsculas
                    if user == usuario and pwd == contrasena:
                        print(f"[+] Credenciales válidas para el usuario: {usuario}")
                        return True
                    elif user == usuario and pwd != contrasena:
                        print(f"[!] Contraseña incorrecta para el usuario: {usuario}")
                        return False
    
    except FileNotFoundError:
        print(f"[!] Error crítico: No se encontró el archivo password.txt")
        print(f"[!] Asegúrate de que el archivo existe en el directorio actual")
        return False
    except PermissionError:
        print(f"[!] Error: No hay permisos para leer el archivo password.txt")
        return False
    except Exception as e:
        print(f"[!] Error inesperado: {e}")
        return False
    
    # Si llegamos aquí, el usuario no existe
    print(f"[!] El usuario '{usuario}' no está registrado")
    return False



def signal_handler(sig, frame):
    """ Maneja la señal de Ctrl+C """
    global ejecutando
    print("\n[!] Recibida señal de interrupción. Cerrando servidor...")
    ejecutando = False
    sys.exit(0)


def hilos_cliente(socket_cliente, clientes, usuarios):
    nombre_usuario = None  # Inicializar para el bloque finally
    
    try:
        # Establecer timeout para la autenticación
        socket_cliente.settimeout(30.0)  # 10 segundos para autenticarse
        
        try:
            nombre_usuario = socket_cliente.recv(1024).decode()
            contrasena = socket_cliente.recv(1024).decode()
        except socket.timeout:
            print(f"[!] Cliente {socket_cliente.getpeername()} timeout en autenticación")
            socket_cliente.sendall("ERROR: Tiempo de autenticación agotado\n".encode())
            socket_cliente.close()
            return
        except ConnectionResetError:
            print(f"[!] Cliente cerró conexión durante autenticación")
            socket_cliente.close()
            return
        except Exception as e:
            print(f"[!] Error en autenticación: {e}")
            socket_cliente.close()
            return
        
        # Verificar credenciales
        if not comprobar_credenciales(nombre_usuario, contrasena):
            print(f"[!] Credenciales incorrectas para usuario: {nombre_usuario}")
            socket_cliente.sendall("ERROR: Credenciales incorrectas".encode())
            socket_cliente.close()
            return
        
        # Credenciales correctas
        print(f"[+] Usuario:{nombre_usuario} autenticado correctamente")
        socket_cliente.sendall("✅ OK: Autenticación exitosa\n".encode())
        
        # Restablecer timeout para el chat normal
        socket_cliente.settimeout(None)
        
        # Registrar usuario
        usuarios[socket_cliente] = nombre_usuario
        print(f"[+] El usuario {nombre_usuario} se ha conectado")
        
        # Notificar a otros usuarios
        for cliente in clientes:
            if cliente is not socket_cliente:
                try:
                    cliente.sendall(f"\n[+] El usuario {nombre_usuario} ha entrado al chat\n\n".encode())
                except:
                    pass
        
        # Bucle principal del chat
        while ejecutando:
            try:
                socket_cliente.settimeout(1.0)
                mensaje = socket_cliente.recv(4096).decode()
                socket_cliente.settimeout(None)
                
                if not mensaje:
                    break
                    
                if "!usuarios" in mensaje.strip():
                    lista_usuarios = ', '.join(usuarios.values())
                    socket_cliente.sendall(f"\n[+] Usuarios conectados ({len(usuarios)}): {lista_usuarios}\n\n".encode())
                    continue
                
                # Reenviar mensaje a otros clientes
                for cliente in clientes:
                    if cliente is not socket_cliente:
                        try:
                            cliente.sendall(f"{mensaje}\n".encode())
                        except:
                            pass
            except socket.timeout:
                continue
            except ConnectionResetError:
                print(f"[!] Conexión reset por {nombre_usuario}")
                break
            except Exception as e:
                print(f"[!] Error en bucle de mensajes para {nombre_usuario}: {e}")
                break
                
    except Exception as e:
        print(f"[!] Error general en hilo de {nombre_usuario or 'desconocido'}: {e}")
    
    finally:
        # Limpiar recursos del cliente (SIEMPRE se ejecuta)
        try:
            socket_cliente.close()
        except:
            pass
        
        # Remover de listas solo si estaba registrado
        if socket_cliente in clientes:
            clientes.remove(socket_cliente)
            
        if nombre_usuario and socket_cliente in usuarios:
            usuario_eliminado = usuarios.pop(socket_cliente, None)
            print(f"[-] El usuario {usuario_eliminado} se ha desconectado")
            
            # Notificar a otros usuarios sobre la desconexión
            for cliente in clientes:
                try:
                    cliente.sendall(f"\n[-] El usuario {usuario_eliminado} ha abandonado el chat\n\n".encode())
                except:
                    pass
        elif nombre_usuario:
            print(f"[-] El usuario {nombre_usuario} se desconectó sin autenticar completamente")
        else:
            print(f"[-] Cliente desconectado durante autenticación")


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
    
    host = 'localhost'
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
    
    # Crear contexto SSL
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="cert-key/server-cert.pem", keyfile="cert-key/server-key.key")
        # Envolver el socket con SSL
        socket_servidor = context.wrap_socket(socket_servidor, server_side=True)
    except Exception as e:
        print(f"[!] Error al configurar SSL: {e}")
        print("[!] Asegúrate de que los archivos server-cert.pem y server-key.key existen")
        return
    
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
