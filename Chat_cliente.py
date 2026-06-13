## Chat multiusuario ##
# Cliente #
#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import socket
import threading
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import ssl
import sys

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


def ventana_autenticacion():
    """Ventana gráfica para autenticación de usuario"""
    
    # Variable para almacenar el resultado
    resultado = {"usuario": None, "contrasena": None, "aceptar": False}
    
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Chat Multiusuario - Inicio de Sesión")
    ventana.geometry("450x500")
    ventana.configure(bg='#1e1e1e')
    
    # Centrar ventana
    ventana.update_idletasks()
    ancho = 1000
    alto = 600
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    # Hacer que la ventana sea modal (bloquear la ventana principal)
    ventana.transient()
    ventana.grab_set()
    
    # Frame principal con padding
    main_frame = tk.Frame(ventana, bg='#1e1e1e')
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Logo o ícono
    try:
        from PIL import Image, ImageTk
        icono = Image.open("img/chat_messages.png")
        icono = icono.resize((70, 70), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(icono)
        lbl_logo = tk.Label(main_frame, image=logo, bg='#1e1e1e')
        lbl_logo.image = logo
        lbl_logo.pack(pady=(0, 10))
    except:
        lbl_logo = tk.Label(main_frame, text="💬", font=("Segoe UI", 50), bg='#1e1e1e', fg='#4ec9b0')
        lbl_logo.pack(pady=(0, 10))
    
    # Título
    lbl_titulo = tk.Label(main_frame, text="CHAT MULTIUSUARIO", 
                         font=("Segoe UI", 18, "bold"),
                         bg='#1e1e1e', fg='#4ec9b0')
    lbl_titulo.pack(pady=(0, 5))
    
    lbl_subtitulo = tk.Label(main_frame, text="Inicia sesión para continuar", 
                            font=("Segoe UI", 10),
                            bg='#1e1e1e', fg='#d4d4d4')
    lbl_subtitulo.pack(pady=(0, 30))
    
    # Frame para campos
    campos_frame = tk.Frame(main_frame, bg='#1e1e1e')
    campos_frame.pack(fill="x", pady=10)
    
    # Campo de usuario
    lbl_usuario = tk.Label(campos_frame, text="👤 USUARIO", 
                          font=("Segoe UI", 10, "bold"),
                          bg='#1e1e1e', fg='#d4d4d4')
    lbl_usuario.pack(anchor="w", pady=(0, 5))
    
    entry_usuario = tk.Entry(campos_frame, font=("Segoe UI", 12),
                            bg='#3c3c3c', fg='#ffffff',
                            relief="flat", insertbackground='white')
    entry_usuario.pack(fill="x", pady=(0, 20), ipady=8)
    entry_usuario.focus()
    
    # Campo de contraseña
    lbl_contrasena = tk.Label(campos_frame, text="🔒 CONTRASEÑA", 
                             font=("Segoe UI", 10, "bold"),
                             bg='#1e1e1e', fg='#d4d4d4')
    lbl_contrasena.pack(anchor="w", pady=(0, 5))
    
    entry_contrasena = tk.Entry(campos_frame, font=("Segoe UI", 12),
                               bg='#3c3c3c', fg='#ffffff',
                               relief="flat", insertbackground='white',
                               show="•")
    entry_contrasena.pack(fill="x", pady=(0, 30), ipady=8)
    
    # Label de estado
    lbl_estado = tk.Label(main_frame, text="", 
                         font=("Segoe UI", 9, "italic"),
                         bg='#1e1e1e', fg='#808080')
    lbl_estado.pack(pady=(0, 10))
    
    # Frame para botones
    botones_frame = tk.Frame(main_frame, bg='#1e1e1e')
    botones_frame.pack(fill="x", pady=10)
    
    def aceptar():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get()
        
        if not usuario:
            lbl_estado.config(text="❌ Por favor, ingresa tu usuario", fg="#f48771")
            entry_usuario.focus()
            return
        
        if not contrasena:
            lbl_estado.config(text="❌ Por favor, ingresa tu contraseña", fg="#f48771")
            entry_contrasena.focus()
            return
        
        resultado["usuario"] = usuario
        resultado["contrasena"] = contrasena
        resultado["aceptar"] = True
        ventana.destroy()
    
    def cancelar():
        ventana.destroy()
    
    def on_enter(event):
        aceptar()
    
    entry_usuario.bind("<Return>", lambda e: entry_contrasena.focus())
    entry_contrasena.bind("<Return>", on_enter)
    
    # Botón Aceptar
    btn_aceptar = tk.Button(botones_frame, text="INICIAR SESIÓN", 
                           command=aceptar,
                           bg='#0e639c', fg='#ffffff',
                           font=("Segoe UI", 12, "bold"), relief="flat",
                           cursor="hand2", padx=20, pady=8)
    btn_aceptar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    # Botón Cancelar
    btn_cancelar = tk.Button(botones_frame, text="CANCELAR", 
                            command=cancelar,
                            bg='#3c3c3c', fg='#ffffff',
                            font=("Segoe UI", 12, "bold"), relief="flat",
                            cursor="hand2", padx=20, pady=8)
    btn_cancelar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    # Info adicional
    lbl_info = tk.Label(main_frame, text="💡 Contacta con el administrador para obtener tus credenciales",
                       font=("Segoe UI", 10),
                       bg='#1e1e1e', fg='#808080')
    lbl_info.pack(pady=(20, 0))
    
    # Esperar a que se cierre la ventana
    ventana.wait_window()
    
    return resultado["aceptar"], resultado["usuario"], resultado["contrasena"]


def autenticar_usurio(socket_cliente):
    try:
        # Solicitar credenciales
        autenticado, usuario, contrasena = ventana_autenticacion()
        if not autenticado:
            print("[!] Autenticación cancelada")
            sys.exit(1)
        
        # Enviar credenciales al servidor
        socket_cliente.sendall(usuario.encode())
        socket_cliente.sendall(contrasena.encode())
        # Esperar respuesta del servidor
        respuesta = socket_cliente.recv(1024).decode()
        
        if "OK" in respuesta:
            print(f"{respuesta}")
            return usuario, True
        elif "ERROR" in respuesta:
            print(f"\n❌ {respuesta}")
            return None, False
        else:
            print(f"\n❌ Error desconocido: {respuesta}")
            return None, False
    except KeyboardInterrupt:
        sys.exit(1)
        print("Saliendo ...")


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
        if "!usuarios" in mensaje:
            listar_usuarios(socket_cliente)
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
    host = 'localhost'
    port = 12345
    
    # Socket para las Conexiones con SSL
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Crear contexto SSL para el cliente
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Envolver el socket con SSL
    socket_cliente = context.wrap_socket(socket_cliente, server_hostname=host)
    
    # Conectar al servidor
    socket_cliente.connect((host, port))
    
    #Comprobar la autenticacion 
    usuario, respuesta = autenticar_usurio(socket_cliente)
    
    if respuesta == False:
        print("\n[!] Autenticación fallida. El programa se cerrará.")
        socket_cliente.close()
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    
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
