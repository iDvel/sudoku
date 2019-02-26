import re
import numpy
from collections import Counter
import copy
import logging

logging.basicConfig(level=logging.INFO)


class Sudoku():
    def __init__(self):
        # 存储数独的数组
        # self.l 结构：
        # [[{},{},{},{},{},{},{},{},{}],[...],[...],...]
        # 字典KV: 'num':数字 'candidates':候补数字 'box':宫 'row':行 'col':列
        self.l = self.init_sudoku_list()
        self.initial_list = copy.deepcopy(self.l)  # 保留一份初始数独供完成后对比
        self.init_information()

    def init_information(self):
        self.d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self.one = [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]
        self.two = [self.a4, self.a5, self.a6, self.b4, self.b5, self.b6, self.c4, self.c5, self.c6]
        self.three = [self.a7, self.a8, self.a9, self.b7, self.b8, self.b9, self.c7, self.c8, self.c9]
        self.four = [self.d1, self.d2, self.d3, self.e1, self.e2, self.e3, self.f1, self.f2, self.f3]
        self.five = [self.d4, self.d5, self.d6, self.e4, self.e5, self.e6, self.f4, self.f5, self.f6]
        self.six = [self.d7, self.d8, self.d9, self.e7, self.e8, self.e9, self.f7, self.f8, self.f9]
        self.seven = [self.g1, self.g2, self.g3, self.h1, self.h2, self.h3, self.i1, self.i2, self.i3]
        self.eight = [self.g4, self.g5, self.g6, self.h4, self.h5, self.h6, self.i4, self.i5, self.i6]
        self.nine = [self.g7, self.g8, self.g9, self.h7, self.h8, self.h9, self.i7, self.i8, self.i9]
        self.box = [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight, self.nine]
        # 给格子字典添加宫信息   {'box':'0'} {'box':'1'} ...
        for i, box in enumerate(self.box):
            for unit in box:
                unit['box'] = i
        # 行信息
        for ch in 'abcdefghi':
            for i in range(1, 10):
                self.__getattr__(ch + str(i))['row'] = self.d[ch]
        # 列信息
        for i in range(9):
            for ch in 'abcdefghi':
                self.__getattr__(ch + str(i + 1))['col'] = i

    def __getattr__(self, item):
        """转换成数组的 index，self.a1 = self.sudoku_list[0][0], self.i9 = self.sudoku_list[8][8]"""
        x, y = [ch for ch in item]
        if x not in 'abcdefghi' or y not in '123456789':
            raise AttributeError
        row, col = self.d[x], int(y) - 1
        return self.l[row][col]

    def init_sudoku_list(self):
        """创建初始的数独组合"""
        l = []
        i = 0
        while i < 9:
            num = input('请逐行输入数独内容，空白格用空格代替。\n请输入第 {} 行的内容：'.format(i + 1))
            # 输入 x 直接生成一个默认数组
            if num == 'x':
                # l = ['··18·9·6·', '259··34··', '4·8·251··', '84·3··62·', '··768··95', '·9··7···1', '·1623··5·',
                #      '·7··1·2··', '3··4·7···']
                l = ['42··5·3·1', '8·59···4·', '······6··', '·1··7·2··', '···2·5···', '··7·1··3·', '··2······',
                     '·9···71·3', '7·6·8··29']
                break
            if re.match(r'[1-9(\s?)]{9}', num) and len(num) == 9:
                num = num.replace(' ', '·')
                l.append(num)
                i += 1
            else:
                print('输入错误，清重新输入。', end='')
                continue
        # 一维数组转二维
        l = [[i for i in j] for j in l]
        # 格子改成字典：num:数字 candidates:候补数字 box:所在宫
        new_l = []
        for i in range(9):
            new_l.append(list(map(lambda x: {'num': x, 'candidates': 'X'}, l[i])))
        # 已知数字的格子的 candidates 改为 [1][2] 这种的
        for i in range(9):
            for j in range(9):
                if new_l[i][j]['num'] is not '·':
                    new_l[i][j]['candidates'] = '[' + new_l[i][j]['num'] + ']'
        return numpy.array(new_l)

    def show(self, l=None):
        if l is None:
            l = self.l
        """图形化显示数独数组"""
        base_graph = '''
        +-------+-------+-------+
        | {0[0][0][num]} {0[0][1][num]} {0[0][2][num]} | {0[0][3][num]} {0[0][4][num]} {0[0][5][num]} | {0[0][6][num]} {0[0][7][num]} {0[0][8][num]} |
        | {0[1][0][num]} {0[1][1][num]} {0[1][2][num]} | {0[1][3][num]} {0[1][4][num]} {0[1][5][num]} | {0[1][6][num]} {0[1][7][num]} {0[1][8][num]} |
        | {0[2][0][num]} {0[2][1][num]} {0[2][2][num]} | {0[2][3][num]} {0[2][4][num]} {0[2][5][num]} | {0[2][6][num]} {0[2][7][num]} {0[2][8][num]} |
        +-------+-------+-------+
        | {0[3][0][num]} {0[3][1][num]} {0[3][2][num]} | {0[3][3][num]} {0[3][4][num]} {0[3][5][num]} | {0[3][6][num]} {0[3][7][num]} {0[3][8][num]} |
        | {0[4][0][num]} {0[4][1][num]} {0[4][2][num]} | {0[4][3][num]} {0[4][4][num]} {0[4][5][num]} | {0[4][6][num]} {0[4][7][num]} {0[4][8][num]} |
        | {0[5][0][num]} {0[5][1][num]} {0[5][2][num]} | {0[5][3][num]} {0[5][4][num]} {0[5][5][num]} | {0[5][6][num]} {0[5][7][num]} {0[5][8][num]} |
        +-------+-------+-------+
        | {0[6][0][num]} {0[6][1][num]} {0[6][2][num]} | {0[6][3][num]} {0[6][4][num]} {0[6][5][num]} | {0[6][6][num]} {0[6][7][num]} {0[6][8][num]} |
        | {0[7][0][num]} {0[7][1][num]} {0[7][2][num]} | {0[7][3][num]} {0[7][4][num]} {0[7][5][num]} | {0[7][6][num]} {0[7][7][num]} {0[7][8][num]} |
        | {0[8][0][num]} {0[8][1][num]} {0[8][2][num]} | {0[8][3][num]} {0[8][4][num]} {0[8][5][num]} | {0[8][6][num]} {0[8][7][num]} {0[8][8][num]} |
        +-------+-------+-------+'''
        base_graph = base_graph.format(l)
        print(base_graph)

    def show_candidates(self, l=None):
        if l == None:
            l = self.l
        """图形化显示数独候选数字"""
        base_graph = '''
        +----------------------------+----------------------------+----------------------------+
        | {0[0][0][candidates]:^9}{0[0][1][candidates]:^9}{0[0][2][candidates]:^9}| {0[0][3][candidates]:^9}{0[0][4][candidates]:^9}{0[0][5][candidates]:^9}| {0[0][6][candidates]:^9}{0[0][7][candidates]:^9}{0[0][8][candidates]:^9}|
        | {0[1][0][candidates]:^9}{0[1][1][candidates]:^9}{0[1][2][candidates]:^9}| {0[1][3][candidates]:^9}{0[1][4][candidates]:^9}{0[1][5][candidates]:^9}| {0[1][6][candidates]:^9}{0[1][7][candidates]:^9}{0[1][8][candidates]:^9}|
        | {0[2][0][candidates]:^9}{0[2][1][candidates]:^9}{0[2][2][candidates]:^9}| {0[2][3][candidates]:^9}{0[2][4][candidates]:^9}{0[2][5][candidates]:^9}| {0[2][6][candidates]:^9}{0[2][7][candidates]:^9}{0[2][8][candidates]:^9}|
        +----------------------------+----------------------------+----------------------------+
        | {0[3][0][candidates]:^9}{0[3][1][candidates]:^9}{0[3][2][candidates]:^9}| {0[3][3][candidates]:^9}{0[3][4][candidates]:^9}{0[3][5][candidates]:^9}| {0[3][6][candidates]:^9}{0[3][7][candidates]:^9}{0[3][8][candidates]:^9}|
        | {0[4][0][candidates]:^9}{0[4][1][candidates]:^9}{0[4][2][candidates]:^9}| {0[4][3][candidates]:^9}{0[4][4][candidates]:^9}{0[4][5][candidates]:^9}| {0[4][6][candidates]:^9}{0[4][7][candidates]:^9}{0[4][8][candidates]:^9}|
        | {0[5][0][candidates]:^9}{0[5][1][candidates]:^9}{0[5][2][candidates]:^9}| {0[5][3][candidates]:^9}{0[5][4][candidates]:^9}{0[5][5][candidates]:^9}| {0[5][6][candidates]:^9}{0[5][7][candidates]:^9}{0[5][8][candidates]:^9}|
        +----------------------------+----------------------------+----------------------------+
        | {0[6][0][candidates]:^9}{0[6][1][candidates]:^9}{0[6][2][candidates]:^9}| {0[6][3][candidates]:^9}{0[6][4][candidates]:^9}{0[6][5][candidates]:^9}| {0[6][6][candidates]:^9}{0[6][7][candidates]:^9}{0[6][8][candidates]:^9}|
        | {0[7][0][candidates]:^9}{0[7][1][candidates]:^9}{0[7][2][candidates]:^9}| {0[7][3][candidates]:^9}{0[7][4][candidates]:^9}{0[7][5][candidates]:^9}| {0[7][6][candidates]:^9}{0[7][7][candidates]:^9}{0[7][8][candidates]:^9}|
        | {0[8][0][candidates]:^9}{0[8][1][candidates]:^9}{0[8][2][candidates]:^9}| {0[8][3][candidates]:^9}{0[8][4][candidates]:^9}{0[8][5][candidates]:^9}| {0[8][6][candidates]:^9}{0[8][7][candidates]:^9}{0[8][8][candidates]:^9}|
        +----------------------------+----------------------------+----------------------------+'''
        base_graph = base_graph.format(l)
        print(base_graph)

    def start(self):
        self.fill_candidates()
        self.fill_num()

    def fill_candidates(self):
        """填充所有潜在数字"""
        self.show_candidates()
        # 查找宫、行、列选出候补数字
        for row in range(9):
            for col in range(9):
                unit = self.l[row][col]
                s = set()
                if unit['num'] is '·':
                    # 统计宫
                    for u in self.box[unit['box']]:
                        s.update(u['num'])
                    # 统计行
                    s.update([u['num'] for u in self.l[row]])
                    # 统计列
                    s.update([u['num'] for u in self.l[:, col]])  # [:, 0] 选择numpy二维数组的第0列
                    # 完成，填充candidates
                    s.remove('·')
                    s = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} - s
                    unit['candidates'] = ''.join(sorted(list(s)))
        print('{:^100}'.format('*** 潜在数字填写完毕 ***'), end='')
        self.show_candidates()

    def fill_num(self):
        """扫看+候补+剔除"""
        # 扫看：潜在数字在当前宫唯一，则此格为此数。 扫到直到无变化
        l_tem = copy.deepcopy(self.l)
        while True:
            self.methed_saokan()
            if (l_tem == self.l).all():
                print('{:^100}'.format('*** 扫看循环结束 ***'), end='')
                self.show()
                break
            else:
                l_tem = copy.deepcopy(self.l)

    def methed_saokan(self):
        # TODO 应该寻找到只出现一次的格子后就记录位置，这么写太麻烦了
        l = []
        for i in range(9):
            # 找到那个只出现一次的数字
            for unit in self.box[i]:
                if '[' not in unit['candidates']:
                    l.extend(unit['candidates'])
            only_one_list = [k for k, v in Counter(l).items() if v == 1]
            l = []
            # 通过这个数字反推格子位置
            for unit in self.box[i]:
                if '[' not in unit['candidates']:
                    for one in only_one_list:
                        if one in unit['candidates']:
                            index = self.box[i].index(unit)
                            # 将数字和候选数字都修改为[x]
                            self.box[i][index]['candidates'] = '[{}]'.format(one)
                            self.box[i][index]['num'] = '{}'.format(one)
                            # 删除同行的相同候选数字
                            row = self.box[i][index]['row']
                            ch = [k for k, v in self.d.items() if v == row][0]
                            for j in range(1, 10):
                                if one in self.__getattr__(ch + str(j))['candidates']:
                                    self.__getattr__(ch + str(j))['candidates'] = self.__getattr__(ch + str(j))[
                                        'candidates'].strip(one)
                            # 删除同列的相同候选数字
                            col = self.box[i][index]['col']
                            for ch in 'abcdefghi':
                                if one in self.__getattr__(ch + str(col + 1))['candidates']:
                                    self.__getattr__(ch + str(col + 1))['candidates'] = \
                                        self.__getattr__(ch + str(col + 1))['candidates'].strip(one)
        print('{:^100}'.format('*** 扫看完毕 ***'), end='')
        self.show_candidates()
