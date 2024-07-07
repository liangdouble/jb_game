import ctypes
import operator
import random
import cv2
import ddddocr
import pygetwindow as gw
import win32api
import win32con, win32gui, win32ui
import numpy as np
from PIL import Image
from tool import color
import time
import aircv

class win():
    def __init__(self, hwnd):
        self.ocr = ddddocr.DdddOcr()
        self.hwnd = hwnd
        self.w,self.h=gw.Window(self.hwnd).size
    def getpic(self,A):
        w_A = A[2] - A[0]
        h_A = A[3] - A[1]
        #w, h = gw.Window(self.hwnd).size
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, w_A, h_A)
        self.saveDC.SelectObject(self.saveBitMap)
        # w_A = A[2] - A[0]
        # h_A = A[3] - A[1]
        self.saveDC.BitBlt((0, 0), (w_A, h_A), self.mfcDC, (A[0], A[1]), win32con.SRCCOPY)
        # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        ###获取位图信息
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)
        ###生成图像
        im_PIL_TEMP = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        self.img = cv2.cvtColor(np.asarray(im_PIL_TEMP), cv2.COLOR_RGB2BGR)
        return self.img
    def findpicAll(self, Target, A=[0,0,900,999],zqd=0.9):
        if A[3]==999:
            A[2]=self.w
            A[3]=self.h
        target =self.getpic(A)
        # Target = Target.split(".")
        # Target = f"{Target[0]}{self.hwnd}.{Target[1]}"
        #cv2.imwrite("1.jpg",target)
        # cv2.destroyAllWindows()
        template = cv2.imread(Target)
        pic_h, pic_w, _ = template.shape
        # 获得模板图片的高宽尺寸
        theight, twidth = template.shape[:2]
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= zqd)
        cooX = []
        cooY = []
        for i in range(len(locations[0])):
            if len(cooX) == 0:
                cooX.append(locations[0][i] + A[0] + pic_w / 2)
                cooY.append(locations[1][i] + A[1] + pic_h / 2)
            else:
                a = np.array(cooX) - locations[0][i]
                b = np.array(cooY) - locations[1][i]
                add = 1
                for p in range(len(a)):
                    if abs(a[p])-A[0]-pic_w/2 < 10 and abs(b[p])-A[1]-pic_h/2 < 10:
                        add = 0
                        break
                if add == 1:
                    cooX.append(locations[0][i]+A[0]+pic_w/2)
                    cooY.append(locations[1][i]+A[1]+pic_h/2)
        return [cooX,cooY,len(cooX)]
    def findpic(self, Target,A=[0,0,900,999],zqd=0.9):
        if A[3]==999:
            A[2]=self.w
            A[3]=self.h
        target =self.getpic(A)
        template = cv2.imread(Target)
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #print(min_val, max_val, min_loc, max_loc )
        strmin_val = str(min_val)
        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.mfcDC.DeleteDC()
        self.saveDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)
        pic_h,pic_w,_=template.shape
        if abs(float(strmin_val)) <=(1-zqd) and min_loc[0] != 0 and min_loc[1] != 0:
            return min_loc[0]+A[0] + int(pic_w/2), min_loc[1]+A[1] +int(pic_h/2)
        else:
            return 0, 0
    def cmpcolor(self,x,y,color1,zqd=0.99,click=0):
        A=[x,y,x+1,y+1]
        target=self.getpic(A)[0][0]
        target2=color.Hex_to_RGB(color1)
        a=np.array(target)-np.array(target2)
        ret=True
        for i in range(len(a)):
            if a[i]/255>1-zqd:
                ret=False
                break
        if click==1 and ret:
            self.click(x,y)
        return ret
    def cmpcolorEx(self,color1,zqd=0.99,click=0):
        colors=color1.split(",")
        click1=colors[0].split("|")
        for i in range(len(colors)):
            zb=colors[i].split("|")
            print(zb)
            zb[0]=int(zb[0])
            zb[1] =int(zb[1])
            A=[zb[0],zb[1],zb[0]+1,zb[1]+1]
            print(A)
            target=self.getpic(A)[0][0]

            target2=color.Hex_to_RGB(zb[2])
            print(self.getpic(A))
            print(target2,22)
            a=abs(np.array(target)-np.array(target2))
            ret=True
            for i in range(len(a)):
                if a[i]/255>1-zqd:
                    return False
            if click==1 and ret:
                print(click1[0],click1[0],"1111111111111")
                self.click(int(click1[0]),int(click1[1]))
        return ret
    def getcolor(self,x,y):
        A=[x,y,x+1,y+1]
        target=self.getpic(A)[0][0]
        target =color.RGB_to_Hex(target)
        return target

    def getstr(self,A=[0, 0, 0, 0]):
        img=self.getpic(A)
        success, encoded_image = cv2.imencode(".png", img)
        img_bytes = np.array(cv2.imencode('.png', img)[1]).tobytes()
        img_bytes = encoded_image.tostring()
        return self.ocr.classification(img_bytes)
    def findcolor(self,res,A=[0, 0, 0, 0],sim=0.9):
        img = self.getpic(A)
        BGR=color.Hex_to_BGR(res)
        for a in range(len(img)):
            for b in range(len(img[0])):
                like=abs((np.array(BGR) - np.array(img[a, b]))) /255
                could = 1
                for i in like:
                    if i > 1-sim:
                        could = 0
                        break
                if could==1:
                    print(img[a, b], a, b)
                    return [A[0] + b, A[1] + a]
        return False
    def findMultiColor(self,x1,y1,x2,y2,color1,color2,sim=0.9,click=0):
        img = self.getpic([x1,y1,x2,y2])
        RGB = color.Hex_to_RGB(color1)
        # print(RGB)
        # print(img[0][0])
        # print(color.RGB_to_Hex(img[0][0]))
        color2=color2.split(",")
        cha=(abs(np.array(img)-np.array(RGB)))/255
        # print(cha)
        for b in range(len(img)):
            for a in range(len(img[0])):
                could = 1
                for i in cha[b][a]:
                    if i>1-sim:
                        could=0
                        break
                if could==1:
                    for i in range(len(color2)):
                        lscolor=color2[i].split("|")
                        xx1=a+int(lscolor[0])
                        yy1=b+int(lscolor[1])
                        RGB=color.Hex_to_RGB(lscolor[2])
                        if x2 - x1 > xx1 > -1 and y2 - y1 > yy1 > -1:
                            imgg=img[yy1][xx1]
                            tryy=np.array(imgg)-np.array(RGB)
                            tryy=tryy>1-sim
                            if np.any(tryy == True):
                                could = 0
                                break
                    if could == 1:

                        if click == 1 and x1 > -1:
                            self.click(int(x1+a), int(y1+b))
                        return [x1+a,y1+b]
            if could == 1:
                break
        return False
    def findMultiColorGood(self,x1,y1,x2,y2,color1,color2="",sim=0.9,click=0):
        img = self.getpic([x1,y1,x2,y2])
        RGB = color.Hex_to_RGB(color1)
        cooX=[]
        cooY=[]
        color2 = color2.split(",")
        cha=(abs(np.array(img)-np.array(RGB)))/255
        # print(cha)
        for b in range(len(img)):
            for a in range(len(img[0])):
                could = 1
                for i in cha[b][a]:
                    if i>1-sim:
                        could=0
                        break
                if could==1:
                    if len(color2)>1:
                        for i in range(len(color2)):
                            lscolor = color2[i].split("|")
                            #print(lscolor)
                            xx1 = a + int(lscolor[0])
                            yy1 = b + int(lscolor[1])
                            RGB = color.Hex_to_RGB(lscolor[2])
                            if x2-x1>xx1>-1 and y2-y1>yy1>-1:
                                imgg = img[yy1][xx1]
                                tryy = np.array(imgg) - np.array(RGB)
                                tryy = tryy > 1 - sim
                                if np.any(tryy == True):
                                    could = 0
                                    break
                            else:
                                break
                    if could == 1:
                        cooX.append(a)
                        cooY.append(b)
        ret=100
        xx1=-1
        yy1=-1
        for i in range(len(cooX)):
            lsssum=np.sum(cha[cooY[i]][cooX[i]])
            if ret>lsssum:
                ret=lsssum
                xx1=cooX[i]
                yy1=cooY[i]

        if click==1 and xx1>-1:
            self.click(int(xx1+x1),int(yy1+y1))
        return [xx1+x1,yy1+y1]
    def findMultiColorAll(self,x1,y1,x2,y2,color1,color2="",sim=0.9,click=0):
        img = self.getpic([x1,y1,x2,y2])
        RGB = color.Hex_to_RGB(color1)
        cooX=[]
        cooY=[]
        color2 = color2.split(",")
        cha=(abs(np.array(img)-np.array(RGB)))/255
        # print(cha)
        for b in range(len(img)):
            for a in range(len(img[0])):
                could = 1
                for i in cha[b][a]:
                    if i>1-sim:
                        could=0
                        break
                if could==1:
                    for i in range(len(color2)):
                        lscolor = color2[i].split("|")
                        #print(lscolor)
                        xx1 = a + int(lscolor[0])
                        yy1 = b + int(lscolor[1])
                        RGB = color.Hex_to_RGB(lscolor[2])
                        if x2-x1>xx1>-1 and y2-y1>yy1>-1:
                            imgg = img[yy1][xx1]
                            tryy = np.array(imgg) - np.array(RGB)
                            tryy = tryy > 1 - sim
                            if np.any(tryy == True):
                                could = 0
                                break
                        else:
                            break
                    if could == 1:
                        cooX.append(a)
                        cooY.append(b)
        cooX=np.array(cooX)+x1
        cooY = np.array(cooY) + y1
        # print(cooX[0])
        # print(cooY[0],click)
        if len(cooX)>0 and click!=0:
            self.click(int(cooX[0]),int(cooY[0]))
        return [cooX,cooY]
    def movein(self, new_x, new_y):
        if new_y is not None and new_x is not None:
            point = (new_x, new_y)
            win32api.SetCursorPos(point)
            self.x = new_x
            self.y = new_y
    def click(self, x, y, bor=True):
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
        print(astrToint)
        for item in astrToint:
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, ord(item), 0)

    # for char in string:
    #     win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)

    def move(self, x1, y1, x2, y2):
        point = win32api.MAKELONG(x1, y1)  # 定义起始点
        point1 = win32api.MAKELONG(x2, y2)  # 定义终点
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, ((y1) << 16 | (x1)))  # 起始点按住
        time.sleep(1)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, point1)  # 移动到终点
        time.sleep(1)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, 0)  # 松开
        time.sleep(1)
