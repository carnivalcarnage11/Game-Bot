# Arda Mavi
import os
import sys
import platform
import numpy as np
from time import sleep
from PIL import ImageGrab, Image
from game_control import *
from predict import predict
from game_control import get_id
from get_dataset import save_img
from multiprocessing import Process
from keras.models import model_from_json
from pynput.mouse import Listener as mouse_listener
from pynput.keyboard import Listener as key_listener
import time

if platform.system() == 'Windows':
    import ctypes
    import win32gui

def get_screenshot():
    img = ImageGrab.grab()
    img = img.resize((150, 150), Image.BILINEAR)
    img = np.array(img)[:,:,:3].astype('float32')/255.
    return img

def save_event_keyboard(data_path, event, key):
    key = get_id(key)
    data_path = data_path + '/-1,-1,{0},{1}.png'.format(event, key)
    screenshot = get_screenshot()
    save_img(screenshot, data_path)
    return

def save_event_mouse(data_path, x, y):
    data_path = data_path + '/{0},{1},0,0.png'.format(x, y)
    screenshot = get_screenshot()
    save_img(screenshot, data_path)
    return

def listen_mouse():
    data_path = 'Data/Train_Data/Mouse'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_click(x, y, button, pressed):
        save_event_mouse(data_path, x, y)

    def on_scroll(x, y, dx, dy):
        pass
    
    def on_move(x, y):
        pass

    with mouse_listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def listen_keyboard():
    data_path = 'Data/Train_Data/Keyboard'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_press(key):
        save_event_keyboard(data_path, 1, key)

    def on_release(key):
        save_event_keyboard(data_path, 2, key)

    with key_listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

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
            print(f'Window "{window_title}" is now focused. Starting recording!')
            break
        time.sleep(poll_interval)

def main():
    dataset_path = 'Data/Train_Data/'
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # Ask user for window title substring
    if platform.system() == 'Windows':
        title_substring = input('Enter part of the game window title to wait for: ')
        wait_for_window(title_substring)

    # Start to listening mouse with new process:
    Process(target=listen_mouse, args=()).start()
    listen_keyboard()
    return

if __name__ == '__main__':
    main()
