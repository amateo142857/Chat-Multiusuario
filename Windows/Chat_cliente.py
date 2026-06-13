## Chat multiusuario ##
# Cliente Mejorado Visualmente
#!/usr/bin/env python3

import tkinter as tk
import socket
import threading
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import ssl 

# Configuración de colores
COLORES = {
    'fondo_ventana': '#1e1e1e',
    'fondo_chat': '#252526',
    'texto_chat': '#d4d4d4',
    'entrada_texto': '#3c3c3c',
    'texto_entrada': '#ffffff',
    'boton_envio': '#0e639c',
    'boton_secundario': '#3c3c3c',
    'boton_peligro': '#a1260d',
    'texto_boton': '#ffffff',
    'mensaje_usuario': '#4ec9b0',
    'mensaje_sistema': '#808080',
    'mensaje_info': '#9cdcfe'
}

def salir_chat(socket_cliente, usuario, ventana):
    socket_cliente.sendall(f"\n[!] El usuario {usuario} ha abandonado el chat\n\n".encode())
    socket_cliente.close()
    ventana.quit()
    ventana.destroy()

def listar_usuarios(socket_cliente):
    socket_cliente.sendall("!usuarios".encode())

def recibir_mensaje(socket_cliente, text_widget):
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode()
            if not mensaje:
                break
            
            text_widget.configure(state='normal')
            
            # Aplicar colores según el tipo de mensaje
            if "[!]" in mensaje or "ha abandonado" in mensaje or "ha entrado" in mensaje:
                # Mensajes del sistema
                text_widget.insert("end", "─" * 50 + "\n", "center")
                text_widget.insert("end", mensaje.strip() + "\n", "sistema")
                text_widget.insert("end", "─" * 50 + "\n", "center")
            elif "[+]" in mensaje:
                # Mensajes de información
                text_widget.insert("end", mensaje.strip() + "\n", "informacion")
            else:
                # Mensajes normales
                if ">" in mensaje:
                    usuario_msg, texto = mensaje.split(">", 1)
                    text_widget.insert("end", f"{usuario_msg}> ", "usuario")
                    text_widget.insert("end", f"{texto}\n", "mensaje")
                else:
                    text_widget.insert("end", f"{mensaje}\n", "normal")
            
            text_widget.see("end")  # Auto-scroll
            text_widget.configure(state="disabled")
            
        except:
            break

def enviar_mensaje(socket_cliente, usuario, text_widget, entry_widget): 
    mensaje = entry_widget.get()
    if mensaje.strip():  # Evitar enviar mensajes vacíos
        if "/limpiar" in mensaje:
            limpiar_chat(text_widget)
            return
        if "/ayuda" in mensaje:
            mostrar_mensaje_bienvenida(text_widget,usuario)
            return
        
        try:
            socket_cliente.sendall(f"{usuario} > {mensaje}".encode())
            entry_widget.delete(0, "end")
            
            # Mostrar mensaje localmente con estilo
            text_widget.configure(state='normal')
            text_widget.insert("end", f"{usuario} > ", "usuario_local")
            text_widget.insert("end", f"{mensaje}\n", "mensaje_local")
            text_widget.see("end")
            text_widget.configure(state="disabled")
        except:
            # Si hay error, mostrar en el chat
            text_widget.configure(state='normal')
            text_widget.insert("end", "[!] Error al enviar el mensaje\n", "sistema")
            text_widget.see("end")
            text_widget.configure(state="disabled")

def limpiar_chat(text_widget):
    text_widget.configure(state='normal')
    text_widget.delete(1.0, "end")
    text_widget.configure(state="disabled")

def configurar_estilos_texto(text_widget):
    """Configurar los estilos para el widget de texto"""
    text_widget.tag_config("usuario", foreground=COLORES['mensaje_usuario'], font=("Segoe UI", 12, "bold"))
    text_widget.tag_config("usuario_local", foreground="#ce9178", font=("Segoe UI", 12, "bold"))
    text_widget.tag_config("mensaje", foreground=COLORES['texto_chat'], font=("Segoe UI", 12))
    text_widget.tag_config("mensaje_local", foreground="#ce9178", font=("Segoe UI", 12))
    text_widget.tag_config("sistema", foreground=COLORES['mensaje_sistema'], font=("Segoe UI", 12, "italic"), justify="center")
    text_widget.tag_config("informacion", foreground=COLORES['mensaje_info'], font=("Segoe UI", 12))
    text_widget.tag_config("normal", foreground=COLORES['texto_chat'])
    text_widget.tag_config("center", justify="center")

def mostrar_mensaje_bienvenida(text_widget, usuario):
    """Mostrar mensaje de bienvenida en el chat"""
    text_widget.configure(state='normal')
    text_widget.insert("end", "═" * 60 + "\n", "center")
    text_widget.insert("end", f"✨ ¡Bienvenido al chat, {usuario}! ✨\n", "center")
    text_widget.insert("end", "═" * 60 + "\n", "center")
    text_widget.insert("end", "\n💡 Comandos disponibles:\n", "informacion")
    text_widget.insert("end", "  • !usuarios - Ver lista de usuarios conectados\n", "normal")
    text_widget.insert("end", "  • /limpiar - Limpiar el chat\n", "normal")
    text_widget.insert("end", "  • /ayuda - Mostrar comandos\n", "normal")

    text_widget.configure(state="disabled")

def Cliente():
    # Conexiones #
    host = '192.168.1.2'
    port = 12345
    
    # Socket para las Conexiones con SSL
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Crear contexto SSL para el cliente
    #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    #context.check_hostname = False
    #context.verify_mode = ssl.CERT_NONE
    
    # Envolver el socket con SSL
    #socket_cliente = context.wrap_socket(socket_cliente, server_hostname=host)
    
    # Conectar al servidor
    socket_cliente.connect((host, port))
    
    # Nombre de Usuario 
    usuario = input(f"\n [+] Introduce tu usuario: ")
    socket_cliente.sendall(usuario.encode())
    
    ## Ventana con diseño ##  
    ventana = tk.Tk()
    ventana.title(f"📤 Chat Multiusuario - {usuario}")
    ventana.geometry("1100x600")
    ventana.minsize(800, 500)  # Tamaño mínimo
    ventana.configure(bg=COLORES['fondo_ventana'])
    
    # Configurar grid para responsividad
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)
    
    # Icono de la ventana
    try:
        icono_1 = Image.open("img/chat_messages.png")
        icono_ventana = ImageTk.PhotoImage(icono_1)
        ventana.iconphoto(False, icono_ventana)
    except:
        print("[!] No se pudo cargar el icono")
    
    # Frame principal
    main_frame = tk.Frame(ventana, bg=COLORES['fondo_ventana'])
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=12)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Frame para el chat
    chat_frame = tk.Frame(main_frame, bg=COLORES['fondo_chat'])
    chat_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
    chat_frame.grid_rowconfigure(0, weight=1)
    chat_frame.grid_columnconfigure(0, weight=1)
    
    # Widget de texto con scroll
    text_widget = ScrolledText(chat_frame, state='disabled', wrap=tk.WORD, 
                               font=("Segoe UI", 12), bg=COLORES['fondo_chat'], 
                               fg=COLORES['texto_chat'], relief="flat", 
                               borderwidth=0, padx=10, pady=12)
    text_widget.grid(row=0, column=0, sticky="nsew")
    
    # Configurar estilos de texto
    configurar_estilos_texto(text_widget)
    
    # Frame para entrada de mensaje
    input_frame = tk.Frame(main_frame, bg=COLORES['fondo_ventana'])
    input_frame.grid(row=1, column=0, sticky="ew")
    input_frame.grid_columnconfigure(0, weight=1)
    
    # Campo de entrada de texto
    entry_widget = tk.Entry(input_frame, font=("Segoe UI", 12), 
                           bg=COLORES['entrada_texto'], 
                           fg=COLORES['texto_entrada'],
                           relief="flat", insertbackground='white')
    entry_widget.grid(row=0, column=0, sticky="ew", padx=(0, 12))
    entry_widget.bind("<Return>", lambda e: enviar_mensaje(socket_cliente, usuario, text_widget, entry_widget))
    
    # Botón de enviar
    button_widget = tk.Button(input_frame, text="📤 Enviar", 
                             command=lambda: enviar_mensaje(socket_cliente, usuario, text_widget, entry_widget), 
                             bg=COLORES['boton_envio'], fg=COLORES['texto_boton'],
                             font=("Segoe UI", 12, "bold"), relief="flat", 
                             padx=20, pady=8, cursor="hand2")
    button_widget.grid(row=0, column=1)
    
    # Frame para botones de acción
    buttons_frame = tk.Frame(main_frame, bg=COLORES['fondo_ventana'])
    buttons_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)
    
    # Botón Listar Usuarios
    user_widget = tk.Button(buttons_frame, text="👥 Listar Usuarios", 
                           command=lambda: listar_usuarios(socket_cliente),
                           bg=COLORES['boton_secundario'], fg=COLORES['texto_boton'],
                           font=("Segoe UI", 12), relief="flat", 
                           padx=20, pady=8, cursor="hand2")
    user_widget.grid(row=0, column=0, padx=(0, 5), sticky="ew")
    
    # Botón Limpiar Chat
    clean_widget = tk.Button(buttons_frame, text="🧹 Limpiar Chat", 
                            command=lambda: limpiar_chat(text_widget),
                            bg=COLORES['boton_secundario'], fg=COLORES['texto_boton'],
                            font=("Segoe UI", 12), relief="flat", 
                            padx=20, pady=8, cursor="hand2")
    clean_widget.grid(row=0, column=1, padx=5, sticky="ew")
    
    # Botón Salir
    exit_widget = tk.Button(buttons_frame, text="🚪 Salir", 
                           command=lambda: salir_chat(socket_cliente, usuario, ventana),
                           bg=COLORES['boton_peligro'], fg=COLORES['texto_boton'],
                           font=("Segoe UI", 12, "bold"), relief="flat", 
                           padx=20, pady=8, cursor="hand2")
    exit_widget.grid(row=0, column=2, padx=(5, 0), sticky="ew")
    
    # Barra de estado
    status_bar = tk.Label(ventana, text=f"✅ Conectado como: {usuario} | Servidor: {host}:{port}", 
                          bg=COLORES['boton_secundario'], fg=COLORES['texto_chat'],
                          font=("Segoe UI", 12), relief="sunken", anchor="w", padx=10)
    status_bar.grid(row=1, column=0, sticky="ew")
    
    # Mostrar mensaje de bienvenida
    mostrar_mensaje_bienvenida(text_widget, usuario)
    
    # Iniciar hilo para recibir mensajes
    thread = threading.Thread(target=recibir_mensaje, args=(socket_cliente, text_widget))
    thread.daemon = True
    thread.start()
    
    ventana.mainloop() 
    socket_cliente.close()
    
if __name__ == '__main__':
    Cliente()
