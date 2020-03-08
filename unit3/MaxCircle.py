# Built by Jurio. on 3/8/2020


import random
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class MaxCircle:

    # 构造函数
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = abs(r)

    # 输出最大圆的信息
    def print_circle(self):
        print('圆心:({},{}), 半径:{}\t'.format(self.x, self.y, self.r))

    # 判断是否处于正方形内
    def if_in_range(self):
        left = abs(self.x - self.r)
        right = abs(self.x + self.r)
        upper = abs(self.y + self.r)
        lower = abs(self.y - self.r)
        if max(left, right, upper, lower) > 1:
            return False
        else:
            return True

    # 判断该圆的圆心是否在其他的圆内
    def if_inside(self, c_list):
        if len(c_list) == 0:
            return False
        else:
            i = False
            for c in c_list:
                c_1 = complex(c.x, c.y)
                r_1 = c.r
                dis = abs(complex(self.x, self.y) - c_1)
                if dis <= r_1:
                    i += True
                    break
                else:
                    i += False
            return i

    # 计算两个圆之间的距离
    def distance(self, temp):
        return abs(complex(self.x, self.y) - complex(temp.x, temp.y)) - (self.r + temp.r)

    # 判断对象是否和temp是否重叠
    def if_cross(self, temp):
        d = self.distance(temp)
        if d < 0:
            return True
        elif d >= 0:
            return False

    # 若该圆符合条件则添加到列表
    def if_attend(self, c_list):
        # 判断该圆是否和列表中其他圆有重合部分
        if self.if_in_range():
            attend = True
            if len(c_list) == 0:
                c_list.append(self)
                return True
            else:
                attend = not self.if_inside(c_list)
                for c in c_list:
                    attend = attend and not self.if_cross(c)

                if attend:
                    c_list.append(self)
                    return True
                else:
                    return False
        else:
            return False


# 计算目前区域内圆的最大半径
def max_r(temp, c_list):
    r_list = [1 - temp.x, temp.x + 1, 1 - temp.y, temp.y + 1]
    if not len(c_list) == 0:
        for c in c_list:
            r = c.distance(temp) + temp.r
            r_list.append(r)
    return min(r_list)


# 绘图函数
def plot_result(c_list):
    plt.figure()
    plt.axes().set_aspect('equal')
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    theta = np.linspace(0, 2 * np.pi, 90)
    for c in c_list:
        plt.plot(c.x + c.r * np.cos(theta), c.y + c.r * np.sin(theta), 'k')
    plt.show()


# 优化函数
def optimize_func(c_list):
    return lambda x: 1 - max_r(MaxCircle(x[0], x[1], 0), c_list)


# 计算在给定圆的数量的情况下，r^2最大时对应的圆的列表。方法二
def find_max_c_list(c_num):
    c_list = []
    # 向列表中添加新圆，直到总数符合要求
    while len(c_list) < c_num:
        cir_in_list = len(c_list)
        mod = (cir_in_list + 1) % 4
        if cir_in_list == 0:
            x = 0
            y = 0
        else:
            if mod == 0:
                x = random.uniform(0, 1)
                y = random.uniform(0, 1)
            elif mod == 1:
                x = random.uniform(-1, 0)
                y = random.uniform(0, 1)
            elif mod == 2:
                x = random.uniform(-1, 0)
                y = random.uniform(-1, 0)
            elif mod == 3:
                x = random.uniform(0, 1)
                y = random.uniform(-1, 0)
        c = MaxCircle(x, y, 0)
        max_c = minimize(optimize_func(c_list), (c.x, c.y), method='SLSQP')
        # 将新圆更新为局部最优解，并添加进列表
        c.x = float(max_c.x[0])
        c.y = float(max_c.x[1])
        c.r = max_r(c, c_list)
        c.if_attend(c_list)
    return c_list


# 计算所有圆的r^2之和
def total_r2(c_list):
    r2 = 0
    for c in c_list:
        r2 += math.pow(c.r, 2)
    return r2


if __name__ == "__main__":
    m = 200
    c_list = find_max_c_list(m)
    R2 = total_r2(c_list)
    print("所有圆半径平方和的最大值为\t", R2)
    for c in c_list:
        c.print_circle()
    plot_result(c_list)
