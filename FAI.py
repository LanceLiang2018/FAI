import random
import copy
from tkinter import *
import tkinter.messagebox
# ●○•


# 算法部分
class FAI:
    def __init__(self, w: int, h: int, P1='●○•'):
        # self.CODE_P1 = '●'
        # self.CODE_P2 = '○'
        # self.CODE_BLANK = '　'
        self.P1 = 1
        self.P2 = 2
        self.BLANK = 0
        self.CODE_P1 = ' 1 '
        self.CODE_P2 = ' 2 '
        self.CODE_BLANK = '   '
        # self.CODE_P1 = '●'
        # self.CODE_P2 = '○'
        # self.CODE_BLANK = '.'
        self.CODE = {0: self.CODE_BLANK, 1: self.CODE_P1, 2: self.CODE_P2}
        self.w = w
        self.h = h
        # 五子棋
        self.WIN_COUNT = 5

        # 奇怪的数组定义方式...Python的对象是直接拷贝使用的
        self.map = [[0 for i in range(w)] for i in range(h)]

        # 定义计算权值的时候用的

        self.weights = {
            self.P1: {
                " 1 ": 1,
                " 11 ": 2,
                " 111 ": 3,
                " 1111 ": 3,
                " 12": 0,
                " 112": 1,
                " 1112": 2,
                " 11112": 3,
            },
            self.P2: {
                " 2 ": 1,
                " 22 ": 2,
                " 222 ": 3,
                " 2222 ": 3,
                " 21": 0,
                " 221": 1,
                " 2221": 2,
                " 22221": 3,
            },
        }

    def __str__(self):
        res = self.CODE_BLANK * self.w + self.CODE_BLANK * 2 + '\n'
        for y in self.map:
            res = res + self.CODE_BLANK
            for x in y:
                res = res + self.CODE[x]
            res = res + self.CODE_BLANK + '\n'
        res = res + self.CODE_BLANK * self.w + self.CODE_BLANK * 2
        return res

    def put(self, x: int, y: int, val: int):
        self.map[y][x] = val

    # 检测哪位玩家赢了
    def win(self, player=0):
        if player == 0:
            if self.win(player=self.P1) is True:
                return self.P1
            if self.win(player=self.P2) is True:
                return self.P2
            # 没有分出胜负
            return 0

        # 检查横行
        for y in self.map:
            # 十分低效率的检查方式
            if player not in y:
                continue
            for i in range(len(y)):
                if y[i] == player:
                    check = y[i:i + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        # 检查列
        for i in range(self.w):
            x = []
            for y in self.map:
                x.append(y[i])
            # 十分低效率的检查方式*2
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        # 检查"\\"列，从左上角开始
        for i in range(self.w):
            x = []
            for yi in range(len(self.map)):
                if i + yi < self.w:
                    x.append(self.map[yi][i + yi])
            # 十分低效率的检查方式*3
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        # 检查"\\"列，从左上角开始（到左下角）
        for i in range(self.h):
            x = []
            for xi in range(self.w):
                if i + xi < self.h:
                    x.append(self.map[i][i + xi])
            # 十分低效率的检查方式*4
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        # 检查"//"列，从左上角开始
        for i in range(self.w):
            x = []
            for yi in range(len(self.map)):
                if 0 <= i - yi < self.w:
                    x.append(self.map[yi][i - yi])
            # 十分低效率的检查方式*5
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        # 检查"//"列，从左上角开始（到左下角）
        for i in range(self.h):
            x = []
            for xi in range(self.w):
                if 0 <= i - xi < self.h:
                    x.append(self.map[i][i - xi])
            # 十分低效率的检查方式*6
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check:
                            return True
                        if player == self.P2 and self.P1 not in check:
                            return True

        return False

    def play(self, player: int):
        weights = [[0 for i in range(self.w)] for i in range(self.h)]
        maps = self.__str__().split('\n')

        # for iy in range(len(maps)):
        #     # 检查横向，从左到右
        #     y = maps[iy]
        #     for ix in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[ix:].startswith(k):
        #                 weights[iy - 1][ix + 1] = weights[iy - 1][ix + 1] + self.weights[player][k]
        #     # 检查横向，从右到左
        #     y = maps[iy][::-1]
        #     for ix in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[ix:].startswith(k):
        #                 weights[iy - 1][self.w - (ix + 2)] = weights[iy - 1][self.w - (ix + 2)] + self.weights[player][k]
        #
        # for ix in range(len(maps[0])):
        #     y = ''
        #     for iy in range(len(maps)):
        #         y = y + maps[iy][ix]
        #
        #     # 检查竖向，从上到下
        #     for iy in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[iy:].startswith(k):
        #                 weights[iy - 1][ix - 1] = weights[iy - 1][ix - 1] + self.weights[player][k]
        #
        #     y = y[::-1]
        #     # 检查竖向，从下到上
        #     for iy in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[iy:].startswith(k):
        #                 weights[self.h - (iy - 0)][ix - 1] = weights[self.h - (iy - 0)][ix - 1] + self.weights[player][k]

        # \\斜向，从左上角到右上角
        for ix in range(len(maps[0])):
            y = ''
            for iy in range(len(maps)):
                if ix + iy < len(maps[0]):
                    y = y + maps[iy][ix + iy]

            # 检查\\向，从上到下
            for iy in range(len(y)):
                for k in self.weights[player]:
                    if y[iy:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[iy - 1][ix + iy - 1] = weights[iy - 1][ix + iy - 1] + self.weights[player][k]

            y = y[::-1]
            # 检查竖向，从下到上
            for iy in range(len(y)):
                for k in self.weights[player]:
                    if y[iy:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] = weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] \
                                                                            + self.weights[player][k]

        # \\斜向，从左上角到左下角
        for iy in range(len(maps)):
            y = ''
            for ix in range(len(maps[0])):
                if ix + iy < len(maps[0]):
                    y = y + maps[iy][ix + iy]

            # 检查\\向，从上到下
            for ix in range(len(y)):
                for k in self.weights[player]:
                    if y[ix:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[iy - 1][ix + iy - 1] = weights[iy - 1][ix + iy - 1] + self.weights[player][k]

            # y = y[::-1]
            # # 检查竖向，从下到上
            # for iy in range(len(y)):
            #     for k in self.weights[player]:
            #         if y[iy:].startswith(k):
            #             if ix + iy < len(maps[0]):
            #                 weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] = weights[self.h - (iy - 0)][
            #                                                                          self.w - (ix + iy + 0)] \
            #                                                                      + self.weights[player][k]

        for w in weights:
            print(w)


# UI部分
class FaiUi:
    def __init__(self, w: int, h: int):
        self.fai = FAI(w, h)

        self.root = Tk()
        self.frame = Frame(self.root).grid()

        self.fai.put(1, 4, self.fai.P1)

        self.map = [[None for i in range(w)] for i in range(h)]
        self.func = [[None for i in range(w)] for i in range(h)]

        for y in range(h):
            for x in range(w):
                self.func[y][x] = lambda: print('y:', self.func[copy.deepcopy(y)][x], 'x:', copy.deepcopy(y))

        for y in range(h):
            for x in range(w):
                self.map[y][x] = Button(self.frame,
                                        # command=lambda: self.clicked(tx, ty),
                                        command=self.func[0][0],
                                        text=self.fai.CODE[self.fai.map[y][x]])
                self.map[y][x].grid(row=y, column=x)

        pass

    def clicked(self, x, y):
        print('clicked:', x, ",", y)
        print(self.func[y][x])


# if __name__ == '__main__':
#     fai = FAI(8, 8)
#     # fai.put(0, 4, fai.P2)
#     # fai.put(0, 5, fai.P1)
#     # fai.put(0, 6, fai.P1)
#     # fai.put(0, 7, fai.P1)
#     # fai.put(0, 8, fai.P1)
#     #
#     # fai.put(1, 0, fai.P1)
#     # fai.put(2, 0, fai.P2)
#     # fai.put(3, 0, fai.P2)
#     # fai.put(4, 0, fai.P2)
#     # fai.put(5, 0, fai.P2)
#
#     # fai.put(6, 1, fai.P1)
#     # fai.put(5, 2, fai.P1)
#     # fai.put(4, 3, fai.P1)
#     # fai.put(3, 4, fai.P1)
#     # fai.put(2, 5, fai.P1)
#
#     # fai.put(2, 2, fai.P1)
#     # fai.put(2, 3, fai.P1)
#     # fai.put(2, 4, fai.P1)
#     # fai.put(2, 5, fai.P1)
#     # fai.put(2, 6, fai.P1)
#
#     fai.put(0, 1, fai.P1)
#
#     fai.play(fai.P1)
#     print(fai)
#     print("Player", fai.win(), 'is winner')


if __name__ == '__main__':
    ui = FaiUi(10, 10)
    ui.root.mainloop()
