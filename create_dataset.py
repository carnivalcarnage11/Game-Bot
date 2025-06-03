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
import datetime

if platform.system() == 'Windows':
    import ctypes
    import win32gui

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

def listen_mouse_with_pause(selected_title):
    data_path = 'Data/Train_Data/Mouse'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    def on_click(x, y, button, pressed):
        screenshot = get_screenshot(selected_title)
        if screenshot is not None:
            save_event_mouse(data_path, x, y)
    with mouse_listener(on_move=lambda *a: None, on_click=on_click, on_scroll=lambda *a: None) as listener:
        listener.join()

def listen_keyboard_with_pause(selected_title):
    data_path = 'Data/Train_Data/Keyboard'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    def on_press(key):
        screenshot = get_screenshot(selected_title)
        if screenshot is not None:
            save_event_keyboard(data_path, 1, key)
    def on_release(key):
        screenshot = get_screenshot(selected_title)
        if screenshot is not None:
            save_event_keyboard(data_path, 2, key)
    with key_listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def get_screenshot(selected_title=None):
    if selected_title and platform.system() == 'Windows':
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        if selected_title.lower() not in window_title.lower():
            return None
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

def save_timed_screenshot(data_path, selected_title=None):
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    while True:
        screenshot = get_screenshot(selected_title)
        if screenshot is not None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'{data_path}/{timestamp}.png'
            save_img(screenshot, filename)
            print(f'Saved timed screenshot: {filename}')
        time.sleep(0.5)

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

    print('Select data collection mode:')
    print('1: Event-based (default, saves on key/mouse events)')
    print('2: Timed (saves screenshot every 0.5 seconds)')
    mode = input('Enter 1 or 2: ').strip()

    selected_title = None
    if platform.system() == 'Windows':
        selected_title = select_window()
        wait_for_window(selected_title)

    if mode == '2':
        save_timed_screenshot('Data/Train_Data/Timed', selected_title)
    else:
        Process(target=listen_mouse_with_pause, args=(selected_title,)).start()
        listen_keyboard_with_pause(selected_title)
    return

if __name__ == '__main__':
    main()
