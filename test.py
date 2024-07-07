import time

import pyautogui
import win32gui, win32con
import keyboard

# 确保在调用下面的函数之前，你的鼠标已经移动到了目标窗口上
def get_window_at_mouse_position():
    # 获取当前鼠标位置
    point = pyautogui.position()
    # 将屏幕坐标转换为窗口坐标
    win32gui.ClientToScreen(win32gui.GetForegroundWindow(), point)
    # 根据坐标获取窗口句柄
    hwnd = win32gui.WindowFromPoint((point[0], point[1]))
    return hwnd



def on_shortcut():
    print("快捷键被触发了!")
    handle = get_window_at_mouse_position()
    print(f"The handle of the window under the mouse is: {handle}")


# 设置快捷键，例如 Ctrl + Shift + A
keyboard.add_hotkey('alt+1', on_shortcut)

# 开始监听键盘事件
keyboard.wait()