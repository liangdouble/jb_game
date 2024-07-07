import cv2
import ddddocr
import pygetwindow as gw
import win32con,win32gui,win32ui
import numpy as np
from PIL import Image
from tool

class win():
    def __init__(self, hwnd):
        self.ocr = ddddocr.DdddOcr()
        self.hwnd = hwnd

    def window_capture(self, Target,zqd=0.9):

        # 获取句柄窗口的大小

        # rctA = get_window_rect(self.hwnd)
        # rctA = list(rctA)
        # print(rctA)
        # w = rctA[2] - rctA[0]
        # h = rctA[3] - rctA[1]
        w_A,h_A=gw.Window(self.hwnd).size
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w_A, h_A)
        saveDC.SelectObject(saveBitMap)
        # w_A = A[2] - A[0]
        # h_A = A[3] - A[1]
        saveDC.BitBlt((0, 0), (w_A, h_A), mfcDC, (0,0), win32con.SRCCOPY)
        # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        ###获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        ###生成图像
        im_PIL_TEMP = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        img = cv2.cvtColor(np.asarray(im_PIL_TEMP), cv2.COLOR_RGB2BGR)
        target = img
        # Target = Target.split(".")
        # Target = f"{Target[0]}{self.hwnd}.{Target[1]}"
        #cv2.imwrite("1.jpg",target)
        # cv2.destroyAllWindows()
        template = cv2.imread(Target)
        # 获得模板图片的高宽尺寸
        theight, twidth = template.shape[:2]
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        # 归一化处理
        cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
        # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 匹配值转换为字符串
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
        # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
        strmin_val = str(min_val)

        # 绘制矩形边框，将匹配区域标注出来
        # min_loc：矩形定点
        # (min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
        # (0,0,225)：矩形的边框颜色；2：矩形边框宽度
        #cv2.rectangle(target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 225), 2)
        # 显示结果,并将匹配值显示在标题栏上
        #cv2.imshow("MatchResult----MatchingValue=" + strmin_val, target)
        #cv2.waitKey()
        #cv2.destroyAllWindows()


        win32gui.DeleteObject(saveBitMap.GetHandle())
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        pic_h,pic_w,_=template.shape
        if abs(float(strmin_val)) <=(1-zqd) and min_loc[0] != 0 and min_loc[1] != 0:
            return min_loc[0] + int(pic_w/2), min_loc[1] +int(pic_h/2)
        else:
            return 0, 0

    def window_str(self,A=[0, 0, 0, 0],):
        # 获取句柄窗口的大小
        # if pic_id:
        #     json = {'pic_id': pic_id, 'class': 'rxjh'}
        #     requests.post(url='http://47.98.177.143:34971/ImageOCR/', json=json).json()

        # rctA = get_window_rect(self.hwnd)
        # rctA = list(rctA)
        #
        # w = rctA[2] - rctA[0]
        # h = rctA[3] - rctA[1]
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]
        #w, h = gw.Window(self.hwnd).size
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w_A, h_A)
        saveDC.SelectObject(saveBitMap)
        # w_A = A[2] - A[0]
        # h_A = A[3] - A[1]
        saveDC.BitBlt((0, 0), (w_A, h_A), mfcDC, (A[0], A[1]), win32con.SRCCOPY)
        # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        ###获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        ###生成图像
        im_PIL_TEMP = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        img = cv2.cvtColor(np.asarray(im_PIL_TEMP), cv2.COLOR_RGB2BGR)
        # if bor:
        #     img = image_binarization(img)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        array_bytes = img.tobytes()  # 或者使用img.tostring()

        # 对数组的图片格式进行编码
        success, encoded_image = cv2.imencode(".png", img)
        img_bytes = np.array(cv2.imencode('.png', img)[1]).tobytes()
        # 将数组转为bytes

        img_bytes = encoded_image.tostring()
        return self.ocr.classification(img_bytes)
    def window_color(self,res,A=[0, 0, 0, 0]):
        #w, h = gw.Window(self.hwnd).size
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w_A, h_A)
        saveDC.SelectObject(saveBitMap)
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]
        saveDC.BitBlt((0, 0), (w_A, h_A), mfcDC, (A[0], A[1]), win32con.SRCCOPY)
        # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        ###获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        ###生成图像
        im_PIL_TEMP = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        img = cv2.cvtColor(np.asarray(im_PIL_TEMP), cv2.COLOR_RGB2BGR)
        BGR=color.Hex_to_BGR(res)
        for a in range(len(img)):
            for b in range(len(img[0])):
                if all(operator.eq(img[a,b],BGR)):
                    print(img[a,b],a,b)
                    return True
        return  False

    def window_imgEX(self,Target,A=[0, 0, 0, 0],ms = 1):

        rctA = get_window_rect(self.hwnd)
        rctA = list(rctA)

        w = rctA[2] - rctA[0]
        h = rctA[3] - rctA[1]
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]

        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w_A, h_A)
        saveDC.SelectObject(saveBitMap)
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]
        saveDC.BitBlt((0, 0), (w_A, h_A), mfcDC, (A[0], A[1]), win32con.SRCCOPY)
        # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        ###获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        ###生成图像
        im_PIL_TEMP = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        img = 255 * np.array(im_PIL_TEMP).astype('uint8')
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        if ms:
            a = aircv.find_template(img, Target, threshold=0.8)
            return a
        else:
            return aircv.find_sift(img,Target)

    def mouse_move(self, new_x, new_y):
        if new_y is not None and new_x is not None:
            point = (new_x, new_y)
            win32api.SetCursorPos(point)
            self.x = new_x
            self.y = new_y

    def click_point(self, x, y, bor=True):
        if bor:
            x = x +random.randint(10,10)
            y = y +random.randint(10,10)

        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, ((y) << 16 | (x)));
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, ((y) << 16 | (x)));

    def send_enter(self):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, 74, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, 74, 0)

    def send_str(self, text):
        astrToint = [ord(c) for c in text]
        for item in astrToint:
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, item, 0)

    def move(self, x1, y1, x2, y2):
        point = win32api.MAKELONG(x1, y1)  # 定义起始点

        point1 = win32api.MAKELONG(x2, y2)  # 定义终点
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, ((y1) << 16 | (x1)))  # 起始点按住
        time.sleep(1)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, point1)  # 移动到终点
        time.sleep(1)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, 0)  # 松开
        time.sleep(1)

    def get_window_rect(self):
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.hwnd),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            return [rect.left, rect.top, rect.right, rect.bottom]