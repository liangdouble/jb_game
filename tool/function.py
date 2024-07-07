import win32gui


def getPointOnLine(x1, y1, x2, y2, n):
    """
        鼠标坐标集合移动算法
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return int(round(x)), int(round(y))
def get_title(hwnd, name):
    title = win32gui.GetClassName(hwnd)
    if title == name:
        return hwnd


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