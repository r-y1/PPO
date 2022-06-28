# 导入库信息
import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

# 设定环境信息
UNIT = 20   # 设定是像素大小为40
MAZE_H = 26  # 设置纵轴的格子数量
MAZE_W = 26  # 设置横轴的格子数量

# 创建一个迷宫类
class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        # 定义动作空间为上下左右四个动作
        self.action_space = ['u', 'd', 'l', 'r']
        # 获取动作数量
        self.n_actions = len(self.action_space)
        # 定义迷宫名字
        self.title('maze')
        # 通过geometry函数来设置窗口的宽和高，分别为格子数量乘以像素大小
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        # 调用迷宫创建函数
        self._build_maze()

        self.count = 0

    def _build_maze(self):
        # 设定画布大小
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # 创建一个个的小格子
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # 创建一个原点
        origin = np.array([10, 510])

        # 创建第一个地狱节点
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            250 - 10, 520 - 440,
            250 + 30, 520 ,
            fill='black')
        # 创建第二个地狱节点
        """
        hell2_center = origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 7.5, hell2_center[1] - 7.5,
            hell2_center[0] + 7.5, hell2_center[1] + 7.5,
            fill='black')
        """
        # 创建一个圆形的天堂节点
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            510 - 7.5, 510 - 7.5,
            510 + 7.5, 510 + 7.5,
            fill='yellow')

        # 创建红色探索得智能体
        self.rect = self.canvas.create_rectangle(
            origin[0] - 7.5, origin[1] - 7.5,
            origin[0] + 7.5, origin[1] + 7.5,
            fill='red')

        # ppack函数的作用是让画布显示中正确的位置上。如果没调用这个函数，就不会正常地显示任何东西。
        self.canvas.pack()
    # 定义重置函数
    def reset(self):
        self.update()
        # 设定重置函数延迟0.5秒
        #time.sleep(0.5)
        # 重置的时候删除原来智能体位置，然后重新设定其在原点
        self.canvas.delete(self.rect)
        origin = np.array([10, 510])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 7.5, origin[1] - 7.5,
            origin[0] + 7.5, origin[1] + 7.5,
            fill='red')
        # 返回重置后的位置
        return self.canvas.coords(self.rect)
    # 定义每步探索函数
    def step(self, action):
        # 首先获取当前的坐标
        action = np.argmax(action)
        #print("action", action)
        self.count += 1
        s = self.canvas.coords(self.rect)
        # 根据动作来定义智能体会如何移动
        base_action = np.array([0, 0])
        if action == 0:   # 向上移动的情况
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # 向下移动的情况
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # 向又移动的情况
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # 向左移动的情况
            if s[0] > UNIT:
                base_action[0] -= UNIT
       # 按照动作移动智能体
        self.canvas.move(self.rect, base_action[0], base_action[1])
       # 移动后的状态定义为s_
        s_ = self.canvas.coords(self.rect)

        #print(self.canvas.coords(self.hell1), type(self.canvas.coords(self.hell1)))

        # 根据移动后的下一个状态，设定奖励值。
        if s_ == self.canvas.coords(self.oval):
            reward = 1e9
            done = True
            self.count = 0
            s_ = 'terminal'
        elif self.count == 1024:
            reward = 0
            done = True
            s_ = 'terminal'
            self.count = 0
        elif (280 >= s_[0] + 7.5 >= 240) and (520 >= s_[1] + 7.5 >= 80) :
            reward = 0
            done = False
            self.canvas.move(self.rect, - base_action[0], - base_action[1])
            s_ = s
        else:
            reward = 0
            done = False
        info = None
       # 返回下一个状态，奖励以及当前Episode是否完成的
        return s_, reward, done, info
    # 刷新当前环境
    def render(self):
        #time.sleep(0.1)
        self.update()

# 刷新函数
def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break
# 自测部分
if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()
