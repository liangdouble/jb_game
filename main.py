import time
from multiprocessing import Process
from tool import color
from model import win
from tool import function
scale = 1

def run(i):
    #print(a[i])
    w=win.win(a[i])
    ##找图点击
    # click = w.window_capture("1.bmp")
    # w.click_point(click[0], click[1])

    # #文字识别
    #print(i, w.window_str([926, 145, 976, 162]))

    #点色识别
    #print(w.window_color("#e7e7e7",[403,81,434,110]))

    #找图
    #print(w.findpic("22.bmp",zqd=0.8))
    #print(w.window_imgEX("1.bmp",[68,303,399,609],0))
    #b=w.findpicAll("22.bmp",[104,88,536,361])

    #色
    #cmpcolorEx(self,color1,zqd=0.99,click=0)
    #print(w.cmpcolorEx("442|177|555663,453|189|ffffff",1))#多点比色
    #print(w.cmpcolor(442, 177, "6f7079|", 1, click=1))  # 比色
    #print(w.getcolor(442,177))
    #print(w.findMultiColor(183,423,242,490, "b20005","-38|30|a60000,-34|31|074ed4",sim=0.99))
    #print(w.findMultiColorGood(183, 423, 242, 490, "b20005", "-38|30|a60000,-34|31|074ed4", sim=0.9))#最优
    #findMultiColorGood(self,x1,y1,x2,y2,color1,color2="",sim=0.9):
    #print(w.findMultiColorAll(183, 423, 242, 490, "b20005", "-38|30|a60000,-34|31|074ed4", sim=0.98))#所有
    #移动
    #w.move(291,413,745,168)
    #w.movein(0,0)
    #输入 不可用
    #w.send_str("asdas")

    #测试
    #print(w.cmpcolorEx("442|177|555663,453|189|ffffff", 1))  # 多点比色
    #print(w.findMultiColorGood(175,297,265,382,"67A950","213|309|F9B29A,204|333|F07448",0.9,1))
   # print(w.cmpcolorEx("213|328|68AA52,213|310|F46A3A",1,1))
    #print(w.findMultiColor(171,296,252,382,"67A94F","211|310|F46838,214|340|A2D192",0.9,1))
   # print(w.findMultiColorAll(167,269,260,398,"61A349","200|323|F36B3B,227|324|F5B49C,213|310|F46A3A",0.9,1))
    print(w.findMultiColorGood(16,17,68,70,"222133","",0.9,0))
a=function.findhwndEX('RenderWindow')
if __name__ == '__main__':
    for i in range(len(a)):
        bb=Process(target=run,args=(0,))
        bb.start()
        #print(color.Hex_to_BGR("#e7e7e7"))





