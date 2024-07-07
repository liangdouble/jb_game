import time

import win32api
import win32con


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