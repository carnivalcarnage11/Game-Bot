# Arda Mavi
import os
import platform
import numpy as np
from time import sleep
from PIL import ImageGrab
from game_control import *
from predict import predict
from game_control import *
from keras.models import model_from_json

if platform.system() == 'Windows':
    import ctypes
    import win32gui
    import threading
    stop_ai = threading.Event()

    def list_windows():
        windows = []
        def enum_handler(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((hwnd, title))
        win32gui.EnumWindows(enum_handler, None)
        return windows

    def select_window():
        windows = list_windows()
        print('Select the game window:')
        for i, (hwnd, title) in enumerate(windows):
            print(f'{i}: {title}')
        idx = int(input('Enter the number of the game window: '))
        return windows[idx][1]  # Return the window title

    def is_selected_window_focused(selected_title):
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        return selected_title.lower() in window_title.lower()

    def alt_listener():
        import keyboard
        while True:
            if keyboard.is_pressed('alt'):
                print('ALT pressed, stopping AI.')
                stop_ai.set()
                break

def wait_for_window(title_substring, poll_interval=1):
    """
    Wait until a window with the given substring in its title is the foreground window.
    """
    if platform.system() != 'Windows':
        print('Window focus detection is only supported on Windows.')
        return
    print(f'Waiting for window with title containing: "{title_substring}" to be focused...')
    while True:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        if title_substring.lower() in window_title.lower():
            print(f'Window "{window_title}" is now focused. Starting AI!')
            break
        sleep(poll_interval)

def main():
    # Get Model:
    model_file = open('Data/Model/model.json', 'r')
    model = model_file.read()
    model_file.close()
    model = model_from_json(model)
    model.load_weights("Data/Model/weights.weights.h5")

    selected_title = None
    if platform.system() == 'Windows':
        selected_title = select_window()
        wait_for_window(selected_title)
        threading.Thread(target=alt_listener, daemon=True).start()

    print('AI start now!')

    while 1:
        if platform.system() == 'Windows' and not is_selected_window_focused(selected_title):
            sleep(0.1)
            continue
        if platform.system() == 'Windows' and stop_ai.is_set():
            print('AI stopped by user.')
            break

        # Get screenshot:
        screen = ImageGrab.grab()
        # Image to numpy array:
        screen = np.array(screen)
        # 4 channel(PNG) to 3 channel(JPG)
        Y = predict(model, screen)
        Y = np.squeeze(Y)
        # If Y is one-hot, get the predicted class
        if len(Y.shape) > 0 and Y.shape[0] > 1:
            pred_class = np.argmax(Y)
        else:
            pred_class = Y
        # You may want to adjust this logic for your specific output
        if np.allclose(Y, 0):
            continue
        # Example: print prediction for debugging
        print('Predicted class:', pred_class, 'Raw output:', Y)
        if pred_class == -1 and int(Y[1]) == -1:
            # Only keyboard action.
            key = get_key(int(Y[3]))
            if int(Y[2]) == 1:
                # Press:
                press(key)
            else:
                # Release:
                release(key)
        elif int(Y[2]) == 0 and int(Y[3]) == 0:
            # Only mouse action.
            click(int(Y[0]), int(Y[1]))
        else:
            # Mouse and keyboard action.
            # Mouse:
            click(int(Y[0]), int(Y[1]))
            # Keyboard:
            key = get_key(int(Y[3]))
            if int(Y[2]) == 1:
                # Press:
                press(key)
            else:
                # Release:
                release(key)

if __name__ == '__main__':
    main()
