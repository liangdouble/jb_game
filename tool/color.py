import base64
import cv2


def RGB_to_Hex(rgb):
    RGB = rgb.split(',')  # 将RGB格式划分开来
    color = '#'
    for i in RGB:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    # print(color)
    return color

def Hex_to_RGB(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    return b, g, r

def Hex_to_BGR(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    return r, g, b

def base642Str(imgBytes):
    base64_data = base64.b64encode(imgBytes)
    return base64_data.decode('utf-8')


def image_binarization(img):
    # 将图片转为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # retval, dst = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
    # 最大类间方差法(大津算法)，thresh会被忽略，自动计算一个阈值
    retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('binary.jpg', dst)
    return dst
