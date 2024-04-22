import turtle
import threading
from time import sleep
import numpy as np

#用于记录径路每个路段节点信息
#三维ijk其中每组第一行分别记录显示状态，径路编号，上下行方向（1上行2下行）
# 0为不显示，1为显示黑色，2为显示绿色
#1号径路在line_pos[1][0][0],第一个空出用来补位
line_pos = np.zeros((61, 6, 3))
for i in range(0,30):
    j=i+1
    line_pos[j*2][0][0] = 0
    line_pos[j*2][0][1] = i+1
    line_pos[j*2][0][2] = 1#该位置标记上下行
    line_pos[j*2-1][0][0] = 0
    line_pos[j*2-1][0][1] = i+1
    line_pos[j*2-1][0][2] = 2  # 该位置标记上下行
#print(line_pos)
#将D30都输入进去
line_pos[59][0][0]=1
line_pos[60][0][0]=1

t=None
flag_end=0
route_node=[30]#经过的红绿灯
line_node=[2,2,1]#选择的线路
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
 [1,  150,  50],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  0,  0],
 [1,  30,  160],
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
 [1,  -180,  100]]


# 定义一个函数用于获取列车位置
def get_position():
    global flag_end
    while True:
        try:
            if flag_end==1:
                return
            x = t.xcor()
            y = t.ycor()
            print("当前位置：({}, {})".format(x, y))
            sleep(0.1)  # 每隔1秒获取一次位置
        except:
            pass

#定义信号灯，通过循环控制
def singal_light(l_type,l_color,fill_color,x_light_pos,y_light_pos):
    l_type.pencolor('black')#线条颜色
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

def line_O(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-400,100)
    l_type.write('-400,100', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-160, 100)
    l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
def line_D30_26_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-160,100)
    l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-120, 160)
    l_type.write('-120,160', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(30, 160)
    l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
def line_D30_26_2(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(-160,100)
    l_type.write('-160,100', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(-120, 100)
    l_type.write('-120,100', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(-80, 50)
    l_type.write('-80,50', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(150, 50)
    l_type.write('150,50', align="center", font=('宋体', 10, 'normal'))
def line_D18_12_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(30,160)
    l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(300, 160)
    l_type.write('300,160', align="center", font=('宋体', 10, 'normal'))
def line_D18_12_2(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(30,160)
    l_type.write('30,160', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(100, 50)
    l_type.write('100,50', align="center", font=('宋体', 10, 'normal'))
    l_type.goto(150, 50)
    l_type.write('150,50', align="center", font=('宋体', 10, 'normal'))
def line_D10_10_1(l_type,l_color,l_lw):
    global t
    l_type.pencolor(l_color)
    l_type.pensize(l_lw)
    #移动时不绘制图形，提起笔
    l_type.penup()
    #将画笔移动到坐标为x, y的位置
    l_type.goto(150,50)
    l_type.write('150,50', align="center", font=('宋体', 10, 'normal'))
    #移动时绘制图形
    l_type.pendown()
    l_type.goto(350, 50)
    l_type.write('350,50', align="center", font=('宋体', 10, 'normal'))
def train_line_map(l_type,l_color,l_lw):
    line = turtle
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
def light_states():
    line = turtle
    line.hideturtle()
    line.delay(0)  # 延迟时间0最小
    line.speed(0)  # 海龟速度0最大 1最慢
    for i in range(len(light_pos)):
        if(light_pos[i][1]==light_pos[i][2]==0):
            pass
        else:
            if(light_pos[i][0]==1):
                singal_light(line, None, 'white',light_pos[i][1],light_pos[i][2])
            else:
                singal_light(line, None, 'black', light_pos[i][1], light_pos[i][2])



def train_route(l_type,l_color,l_lw):
    global flag_end
    color='blue'
    width=2
    if(route_node[0]==30):
        line_O(l_type, color, width)

        if(line_node[0]==1):#选择上行线
            line_D30_26_1(l_type, color, width)
            if(line_node[1]==1):
                line_D18_12_1(l_type, color, width)

            elif(line_node[1] == 2):
                line_D18_12_2(l_type, color, width)
                if(line_node[2] == 1):
                    line_D10_10_1(l_type, color, width)

        elif(line_node[0]==2):#选择下行线
            line_D30_26_2(l_type, color, width)
            if (line_node[2] == 1):
                line_D10_10_1(l_type, color, width)
    flag_end=1
width=2
color='black'
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



# 创建一个新的线程来获取海龟位置
position_thread = threading.Thread(target=get_position)
# 启动线程
position_thread.start()


# 主线程继续执行绘图任务
# 创建一个turtle对象
t = turtle.Turtle()#建立一个海龟
speed = 1#0是最快的
turtle.delay(10)#延迟时间0最小
t.speed(speed)#海龟速度0最大 1最慢
#火车实际运行
train_route(t,'color',2)
print("kaishizou")
# 等待线程结束
position_thread.join()

# 关闭turtle图形窗口
turtle.done()
w.exitonclick()