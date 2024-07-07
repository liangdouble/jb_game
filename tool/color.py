import base64
import cv2


def RGB_to_Hex(rgb):
    if isinstance(rgb, str):
        rgb = rgb.split(',')  # 将RGB格式划分开来
    hex_str = '#{:02x}{:02x}{:02x}'.format(rgb[2], rgb[1], rgb[0])
    # for i in rgb:
    #     num = int(i)
    #     # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
    #     color += str(hex(num))[-2:].replace('x', '0').upper()
    # # print(color)
    return hex_str

def BGR_to_Hex(rgb):
    if isinstance(rgb, str):
        rgb = rgb.split(',')  # 将RGB格式划分开来
    color = '#'
    for i in rgb:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    # print(color)
    return color


def Hex_to_RGB(hex):
    k=0
    if hex[0]=="#":
        k=1
    r = int(hex[k:k+2], 16)
    g = int(hex[k+2:k+4], 16)
    b = int(hex[k+4:k+6], 16)
    return b, g, r

def Hex_to_BGR(hex):
    k=0
    if hex[0]=="#":
        k=1
    r = int(hex[k:k+2], 16)
    g = int(hex[k+2:k+4], 16)
    b = int(hex[k+4:k+6], 16)
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