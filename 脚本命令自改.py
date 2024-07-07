import random
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import string
import time
import win32api
import win32con, win32gui, win32ui
import cv2
import numpy as np
import operator
import ddddocr
import aircv
import ctypes
import pygetwindow as gw
from multiprocessing import Process
from tool import color
from PIL import Image

scale = 1




def getPointOnLine(x1, y1, x2, y2, n):
    """
        鼠标坐标集合移动算法
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return int(round(x)), int(round(y))


def Ocr(self, img, value=None):
    result = []
    resultOcr = self.ocr.ocr(img, cls=True)
    if resultOcr:
        for line in resultOcr:
            if value == line[1][0]:
                result.append([line[0], line[1][0]])
            elif not value:
                result.append([line[0], line[1][0]])
    return result


#def findhwnd(les='LDPlayerMainFrame'):
def findhwnd(les='RenderWindow'):

    all_hwnd = get_all_windows()
    hwnd = []
    for i in all_hwnd:
        hwnds = get_title(i, les)
        if hwnds != None:
            hwnd.append(hwnds)
    return hwnd
def findhwndEX(les):
    all_hwnd = get_all_windows()
    hwnd = []

    for i in all_hwnd:
        hwnds = get_title(i, les)
        if hwnds != None:
            hwnd.append(hwnds)
    if hwnd != []:
        return hwnd
    else:
        hwndson = []
        for i in range(len(all_hwnd)):
            hwnd = get_son_windows(all_hwnd[i])

            for q in range(len(hwnd)):
                h = get_title(hwnd[q], les)
                if h != None:
                    hwndson.append(h)

        return hwndson




def get_son_windows(parent):
    hWnd_child_list = []
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWnd_child_list)
    return hWnd_child_list
def get_all_windows():
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    return hWnd_list

def get_title(hwnd, name):
    title = win32gui.GetClassName(hwnd)
    if title == name:
        return hwnd


class c_keybord(object):
    def __init__(self, handle: HWND):
        """
         https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        :type handle: HWND
        :param handle:
        """
        self.handle = handle
        self.PostMessageW = windll.user32.PostMessageW
        self.MapVirtualKeyW = windll.user32.MapVirtualKeyW
        self.VkKeyScanA = windll.user32.VkKeyScanA
        self.WM_KEYDOWN = 0x100
        self.WM_KEYUP = 0x101

        self.VkCode = {
            "back": 0x08,
            "tab": 0x09,
            "return": 0x0D,
            "shift": 0x10,
            "control": 0x11,
            "menu": 0x12,
            "pause": 0x13,
            "capital": 0x14,
            "escape": 0x1B,
            "space": 0x20,
            "end": 0x23,
            "home": 0x24,
            "left": 0x25,
            "up": 0x26,
            "right": 0x27,
            "down": 0x28,
            "print": 0x2A,
            "snapshot": 0x2C,
            "insert": 0x2D,
            "delete": 0x2E,
            "lwin": 0x5B,
            "rwin": 0x5C,
            "numpad0": 0x60,
            "numpad1": 0x61,
            "numpad2": 0x62,
            "numpad3": 0x63,
            "numpad4": 0x64,
            "numpad5": 0x65,
            "numpad6": 0x66,
            "numpad7": 0x67,
            "numpad8": 0x68,
            "numpad9": 0x69,
            "multiply": 0x6A,
            "add": 0x6B,
            "separator": 0x6C,
            "subtract": 0x6D,
            "decimal": 0x6E,
            "divide": 0x6F,
            "f1": 0x70,
            "f2": 0x71,
            "f3": 0x72,
            "f4": 0x73,
            "f5": 0x74,
            "f6": 0x75,
            "f7": 0x76,
            "f8": 0x77,
            "f9": 0x78,
            "f10": 0x79,
            "f11": 0x7A,
            "f12": 0x7B,
            "numlock": 0x90,
            "scroll": 0x91,
            "lshift": 0xA0,
            "rshift": 0xA1,
            "lcontrol": 0xA2,
            "rcontrol": 0xA3,
            "lmenu": 0xA4,
            "rmenu": 0XA5
        }

    def get_virtual_keycode(self, key: str):
        """根据按键名获取虚拟按键码
        https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        Args:
            key (str): 按键名
        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            return self.VkKeyScanA(ord(key)) & 0xff
        else:
            return self.VkCode[key]

    def key_down(self, vk_code, scan_code):
        """按下指定按键
            https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        Args:
            :param vk_code:
            :param scan_code:
        """

        wparam = vk_code
        lparam = (scan_code << 16) | 1
        self.PostMessageW(self.handle, self.WM_KEYDOWN, wparam, lparam)

    def key_up(self, vk_code, scan_code):
        """放开指定按键
            https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        Args:
            :param vk_code:
            :param scan_code:
        """
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        self.PostMessageW(self.handle, self.WM_KEYUP, wparam, lparam)

    def key_click(self, key: str, wait=0.2):

        vk_code = self.get_virtual_keycode(key)
        scan_code = self.MapVirtualKeyW(vk_code, 0)
        self.key_down(vk_code, scan_code)
        time.sleep(wait)
        self.key_up(vk_code, scan_code)


def getPointOnLine(x1, y1, x2, y2, n):
    """
        鼠标坐标集合移动算法
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return int(round(x)), int(round(y))


class WinMouse(object):
    def __init__(self, handle: int, num_steps=80):
        self.handle = handle
        self.__win32api = win32api
        self.__win32con = win32con
        self.num_steps = num_steps
        self.__width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        self.__high = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴

    def __left_down(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_LBUTTONDOWN, self.__win32con.MK_LBUTTON, param)

    def __left_up(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_LBUTTONUP, None, param)

    def __left_move(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_MOUSEMOVE, self.__win32con.MK_LBUTTON, param)

    def __right_down(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_RBUTTONDOWN, self.__win32con.MK_RBUTTON, param)

    def __right_up(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_RBUTTONUP, None, param)

    def __right_move(self, param):
        self.__win32api.PostMessage(self.handle, self.__win32con.WM_MOUSEMOVE, self.__win32con.MK_RBUTTON, param)

    def left_click(self, x: int, y: int, wait=0.2):
        param = self.__win32api.MAKELONG(x, y)
        self.__left_down(param=param)
        time.sleep(wait)
        self.__left_up(param=param)

    def left_doubleClick(self, x: int, y: int, click=2, wait=0.4):
        wait = wait / click
        param = self.__win32api.MAKELONG(x, y)
        for cou in range(click):
            self.__left_down(param=param)
            time.sleep(wait)
            self.__left_up(param=param)

    def left_click_move(self, x: int, y: int, m_x: int, m_y: int, wait=2):
        param = self.__win32api.MAKELONG(x, y)
        self.__left_down(param)
        steps = [getPointOnLine(x, y, m_x, m_y, n / self.num_steps) for n in range(self.num_steps)]
        steps.append((m_x, m_y))
        wait_amount = wait / self.num_steps
        new_steps = list(set(steps))
        new_steps.sort(key=steps.index)
        for step in new_steps:
            tweenX, tweenY = step
            param = self.__win32api.MAKELONG(tweenX, tweenY)
            self.__left_move(param)
            time.sleep(wait_amount)
        # param = self.__win32api.MAKELONG(m_x, m_y)
        # self.__left_move(param)
        # time.sleep(wait)

        self.__left_up(param)

    def right_click(self, x: int, y: int, wait=0.2):
        param = self.__win32api.MAKELONG(x, y)
        self.__right_down(param=param)
        time.sleep(wait)
        self.__right_up(param=param)

    def right_doubleClick(self, x: int, y: int, click=2, wait=0.4):
        wait = wait / click
        param = self.__win32api.MAKELONG(x, y)
        for cou in range(click):
            self.__right_down(param=param)
            time.sleep(wait)
            self.__right_up(param=param)

    def right_click_move(self, x: int, y: int, m_x: int, m_y: int, wait=2):
        param = self.__win32api.MAKELONG(x, y)
        self.__right_down(param)
        steps = [getPointOnLine(x, y, m_x, m_y, n / self.num_steps) for n in range(self.num_steps)]
        steps.append((m_x, m_y))
        wait_amount = wait / self.num_steps
        new_steps = list(set(steps))
        new_steps.sort(key=steps.index)
        for step in new_steps:
            tweenX, tweenY = step
            param = self.__win32api.MAKELONG(tweenX, tweenY)
            self.__right_move(param)
            time.sleep(wait_amount)
        self.__right_up(param)
def run(i):
    w=win(a[i])
    ##找图点击
    # click = w.window_capture("1.bmp")
    # w.click_point(click[0], click[1])

    ##文字识别
    #print(i,w.window_str([53,225,119,250]))

    ##点色识别
    w.window_color("#e7e7e7",[403,81,434,110])
a=findhwndEX('RenderWindow')
if __name__ == '__main__':
    b=[]
    #for i in range(len(a)):
    bb=Process(target=run,args=(0,))
    bb.start()
    print(Hex_to_BGR("#e7e7e7"))





