#!/usr/bin/env python3
import pyautogui
import math
import time
import threading
from pynput import keyboard, mouse

running = True
programmatic_move = False

# Inicialmente, definimos os listeners como None para podermos referenciá-los dentro da função.
keyboard_listener = None
mouse_listener = None

def move_mouse():
    """Move o mouse em um padrão circular enquanto o programa estiver rodando."""
    global programmatic_move, running
    radius = 50  # Raio do movimento circular
    angle = 0
    while running:
        # Obtém a posição atual do mouse
        current_x, current_y = pyautogui.position()
        # Calcula a nova posição com base no ângulo
        new_x = current_x + radius * math.cos(angle)
        new_y = current_y + radius * math.sin(angle)
        # Indica que o movimento é gerado pelo programa (para ignorar o evento)
        programmatic_move = True
        pyautogui.moveTo(new_x, new_y, duration=0.2)
        programmatic_move = False
        angle += 0.2
        time.sleep(0.1)

def stop_program(*args):
    """
    Encerra o programa se uma interação do usuário for detectada.
    Se a interação for gerada pelo próprio movimento (flag programmatic_move=True), ignora.
    """
    global running, programmatic_move, keyboard_listener, mouse_listener
    # Se o programa já estiver encerrando, não faz nada.
    if not running:
        return
    # Se o evento ocorreu durante um movimento programático, ignora.
    if programmatic_move:
        return
    running = False
    print("Interação detectada. Encerrando...")
    # Para os listeners para evitar novos eventos.
    if keyboard_listener is not None:
        keyboard_listener.stop()
    if mouse_listener is not None:
        mouse_listener.stop()

# Configura os listeners de teclado e mouse
keyboard_listener = keyboard.Listener(on_press=stop_program)
mouse_listener = mouse.Listener(on_move=stop_program, on_click=stop_program)
keyboard_listener.start()
mouse_listener.start()

# Inicia a thread que movimenta o mouse
mouse_thread = threading.Thread(target=move_mouse)
mouse_thread.start()

# Aguarda a finalização dos listeners e da thread de movimento
keyboard_listener.join()
mouse_listener.join()
mouse_thread.join()