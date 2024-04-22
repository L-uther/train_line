import turtle
import threading
from time import sleep
import numpy as np
import pygame
import keyboard
from pynput.keyboard import Key, KeyCode, Listener

turtle.bgcolor("black")
#用于记录径路每个路段节点信息
#三维ijk其中每组第一行分别记录显示状态，径路编号，上下行方向（1上行2下行）
# None为不显示，1为显示黑色，2为显示绿色
#1号径路在line_pos[1][0][0],第一个空出用来补位
line_pos = np.zeros((61, 6, 3))
for i in range(0,30):
    j=i+1
    line_pos[j*2][0][0] = None
    line_pos[j*2][0][1] = i+1
    line_pos[j*2][0][2] = 1#该位置标记上下行
    line_pos[j*2-1][0][0] = None
    line_pos[j*2-1][0][1] = i+1
    line_pos[j*2-1][0][2] = 2  # 该位置标记上下行
#print(line_pos)


t=None
flag_end=0
route_node=[30]#经过的红绿灯
line_node=[1,2,1]#选择的线路
#信号灯的位置
light_pos=[
    [1,0,0],
[ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [ 1,  0,  0],
 [1,  140,  52],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  162],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  -190,  102]]
#信号灯标签的位置
light_label=[[30,-180,100],
[ 18,10,160],
 [ 10,120,50],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0]]
#岔口标签的位置
Fork_label=[[26,-120,100],
[ 12,50,160],
 [ 10,100,50],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0],
 [ 0,  0,  0]]
#定义信号灯，通过循环控制
def singal_light(l_type,l_color,fill_color,x_light_pos,y_light_pos):
    l_type.pencolor('white')#线条颜色
    l_type.fillcolor(fill_color)#信号灯颜色
    r_singal=5#信号灯圆的半径
    #绘制信号的灯的竖线
    l_type.pensize(3)
    l_type.penup()
    l_type.goto(x_light_pos-r_singal, y_light_pos)
    l_type.pendown()
    l_type.goto(x_light_pos-r_singal, y_light_pos+10)
    #绘制信号灯的两个圆，先画左边的
    l_type.pensize(2)
    l_type.begin_fill()
    l_type.pensize(1)
    l_type.delay(0)  # 延迟时间0最小
    l_type.speed(0)  # 0最大 1最慢
    l_type.penup()
    l_type.goto(x_light_pos, y_light_pos)
    l_type.pendown()
    l_type.begin_fill()
    l_type.circle(r_singal)
    l_type.penup()
    l_type.goto(x_light_pos+10, y_light_pos)
    l_type.pendown()
    l_type.circle(r_singal)
    l_type.end_fill()
    l_type.penup()



def test(x):
    a = keyboard.KeyboardEvent('down',28,'a')
    if x.event_type == 'down' and x.name == 'a':
        print("你按下了enter键")
        light_pos[10][0]=0
        print(light_pos[10][0])

# 启动监听
def listener_keyboard():
    #with Listener(on_press=on_press, on_release=on_release) as listener:
    #    listener.join()
    keyboard.hook(test)
    keyboard.wait()
#报警声音
sound_flag=0
def play_mp3():
    while True:
        if(sound_flag==1):
            pygame.mixer.init()
            pygame.mixer.music.load('sound.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(0)
        else:
            pass
def distance_train_signal(x,y):
    distance_m=0
    if(x<-210 and x>-260 and y==100):#信号灯报警
        distance_m =-190-x
        #print("当前位置距离D30信号灯还有{}米，前方D30信号机未开放，距离30米不得越过".format((distance_m)))
        #print("当前位置：({}, {})".format(x, y))
        return 1
    if(x<-170 and x>-200 and y==100):#匝道报警
        distance_m = -120 - x
        #print("当前位置距离26号岔口还有{}米，前方26号道岔未开放，距离30米不得越过".format((distance_m)))
        #print("当前位置：({}, {})".format(x, y))
        return 1
    if (x < -30 and x > -80 and y == 160):  # 信号灯报警
        distance_m = - x
        #print("当前位置距离D18信号灯还有{}米，前方D30信号机未开放，距离30米不得越过".format((distance_m)))
        return 1
    if (x < 20 and x > -20 and y == 160):  # 匝道报警
        distance_m = 50 - x
        #print("当前位置距离12号岔口还有{}米，前方26号道岔未开放，距离30米不得越过".format((distance_m)))
        return 1
    if (x <130 and x >110 and y == 50):  # 信号灯报警
        distance_m =140- x+20
        #print("当前位置距离D10信号灯还有{}米，前方D30信号机未开放，距离30米不得越过".format((distance_m)))
        return 1
    if (x <90 and x > 50 ):  # 匝道报警
        distance_m = 100- x
        #print("当前位置距离10号岔口还有{}米，前方26号道岔未开放，距离30米不得越过".format((distance_m)))
        return 1

# 定义一个函数用于获取列车位置
def get_position():
    global flag_end,sound_flag
    while True:
        try:
            if flag_end==1:
                return
            x = t.xcor()
            y = t.ycor()
            #print("当前位置：({}, {})".format(x, y))
            sleep(0.1)  # 每隔0.1秒获取一次位置
            sound_flag=distance_train_signal(x,y)

        except:
            pass


def line_O(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-400,100)
    #l_type.write('-400,100', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-160, 100)
    #l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
def line_D30_26_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-160,100)
    #l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
    #l_type.goto(-155, 110)
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-120, 160)
    #l_type.write('-120,160', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(30, 160)
    #l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
def line_D30_26_2(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-160,100)
    #l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(-150, 100)
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-30, 100)
    #l_type.write('-30,100', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(20, 55)
    l_type.goto(30, 55)
    #l_type.write('30,55', align="center", font=('宋体', 10, 'normal'))
    #l_type.goto(90, 50)
    #l_type.write('90,50', align="center", font=('宋体', 10, 'normal'))
def line_D18_12_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(30,160)
    #l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(40, 160)
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(300, 160)
    #l_type.write('300,160', align="center", font=('宋体', 10, 'normal'))




    ###########################
    l_type.penup()
    # 将画笔移动到坐标为x, y的位置
    l_type.goto(-400, 50)
    #l_type.write('-400,100', align="center", font=('宋体', 10, 'normal'))
    # 移动时绘制图形
    l_type.pendown()
    l_type.goto(90, 50)
    #l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
def line_D18_12_2(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(30,160)
    #l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
    #l_type.goto(40, 170)
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(100, 50)
    #l_type.write('100,50', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(150, 50)
    #l_type.write('150,50', align="center", font=('宋体', 10, 'normal'))
def line_D10_10_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(150,50)
    #l_type.write('150,50', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(350, 50)
    #l_type.write('350,50', align="center", font=('宋体', 10, 'normal'))

def train_line_map(l_type,l_color,l_lw):
    line = turtle

    color='green'
    width=5
    if(route_node[0]==30):
        line_O(line, color, width)

        if(line_node[0]==1):#选择上行线
            line_D30_26_1(line, color, width)
            if(line_node[1]==1):
                line_D18_12_1(line, color, width)

            elif(line_node[1] == 2):
                line_D18_12_2(line, color, width)
                if(line_node[2] == 1):
                    line_D10_10_1(line, color, width)

        elif(line_node[0]==2):#选择下行线
            line_D30_26_2(line, color, width)
            if (line_node[2] == 1):
                line_D10_10_1(line, color, width)
def light_states():
    line = turtle
    line.hideturtle()
    line.delay(0)  # 延迟时间0最小
    line.speed(0)  # 海龟速度0最大 1最慢
    for i in range(len(light_pos)):
        if(light_pos[i][1]==light_pos[i][2]==0):
            pass
        else:
            if(light_pos[i][0]==1):#开
                singal_light(line, None, 'white',light_pos[i][1],light_pos[i][2])
            else:
                singal_light(line, None, 'black', light_pos[i][1], light_pos[i][2])


def train_route(l_type,l_color,l_lw):
    global flag_end,turtle
    line=l_type

    # 移动时不绘制图形，提起笔
    line.penup()
    # 将画笔移动到坐标为x, y的位置
    line.goto(-400, 100)
    turtle.delay(100)  # 延迟时间0最小
    line.speed(1)  # 海龟速度0最大 1最慢

    color='green'
    width=2
    if(route_node[0]==30):
        line_O(line, color, width)

        if(line_node[0]==1):#选择上行线
            line_D30_26_1(line, color, width)
            if(line_node[1]==1):
                line_D18_12_1(line, color, width)

            elif(line_node[1] == 2):
                line_D18_12_2(line, color, width)
                if(line_node[2] == 1):
                    line_D10_10_1(line, color, width)

        elif(line_node[0]==2):#选择下行线
            line_D30_26_2(line, color, width)
            if (line_node[2] == 1):
                line_D10_10_1(line, color, width)
    flag_end=1
width=2
color='white'#线路颜色
line=turtle
line.hideturtle()
line.delay(0)#延迟时间0最小
line.speed(0)#海龟速度0最大 1最慢

w=line_O(line,color,width)
line_D30_26_1(line,color,width)
line_D30_26_2(line,color,width)
line_D18_12_1(line,color,width)
line_D18_12_2(line,color,width)
line_D10_10_1(line,color,width)
#运行火车规划的线路
train_line_map(line,color,width)
#信号灯颜色
light_states()

#singal_light(line,color,'GREEN',-180,100)


# 创建一个新的线程来获取海龟位置
position_thread1 = threading.Thread(target=get_position)
position_thread2 = threading.Thread(target=play_mp3)
position_thread3 = threading.Thread(target=listener_keyboard)
# 启动线程
position_thread1.start()
position_thread2.start()
position_thread3.start()


t = turtle.Turtle()  # 建立一个海龟
speed = 0  # 0是最快的
turtle.delay(0)  # 延迟时间0最小
t.speed(speed)  # 海龟速度0最大 1最慢
#火车实际运行
train_route(t,'color',2)

# 等待线程结束
position_thread1.join()
position_thread2.join()
position_thread3.join()

# 关闭turtle图形窗口
turtle.done()
w.exitonclick()