import re
import numpy
from collections import Counter
import copy
import logging
import json

logging.basicConfig(level=logging.INFO)


class Sudoku:
    def __init__(self):
        # 计数
        self.saokan_count = 0

    def start(self):
        # 数独二维数组
        self.l = self.init_suduku_list()
        # 保存一份初始数组，供完成后对照
        self.initial_list = copy.deepcopy(self.l)

        # start!
        self.show(key='num')
        self.fill_candidates()
        self.fill_number()

    def init_suduku_list(self):
        """创建初始的数独组合：二维数组"""
        input_l = []
        print("请逐行输入数独内容，空白格用空格键代替，直接回车初始化默认数组")
        i = 1
        while i <= 9:
            num = input('请输入第 {} 行的内容：'.format(i))
            if num == '':
                input_l = ['42··5·3·1',
                           '8·59···4·',
                           '······6··',
                           '·1··7·2··',
                           '···2·5···',
                           '··7·1··3·',
                           '··2······',
                           '·9···71·3',
                           '7·6·8··29']
                break
            elif re.match(r'[1-9(\s)]{9}', num) and len(num) == 9:
                input_l.append(num.replace(' ', '·'))
                i += 1
            else:
                continue
        # 一维数组转二维
        input_l = [[i for i in j] for j in input_l]
        # 格子（unit）转字典，添加相关信息，格式如下
        # [[{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}],
        #  [{}, {}, {}, {}, {}, {}, {}, {}, {}]]
        # num: 初始数字及后期已算出确定的数字
        # can: candidates，候选数字，如果已确定数字则显示为[1]这种格式
        # box: 所在宫 row: 所在行 col: 所在列
        for i, row in enumerate(input_l):
            for j, unit in enumerate(row):
                input_l[i][j] = {'num': unit,
                                 'can': '[{}]'.format(unit) if unit is not '·' else None,
                                 'box': (i // 3) * 3 + (j // 3),
                                 'row': i,
                                 'col': j}
        return input_l

    def get_list_of(self, position, number=None):
        """拿取宫、行、列的列表"""
        if position == 'boxes':
            # 返回包含 9 个宫的二维数组，每一组是一宫
            boxes = []
            for i in range(9):
                boxes.append([unit for row_list in self.l for unit in row_list if unit['box'] == i])
            return boxes
        else:
            # 返回单一宫、行、列的列表
            return [unit for row_list in self.l for unit in row_list if unit[position] == number]

    def show(self, key='can'):
        """图形化显示数独二维数组"""
        if key == 'num':
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
        elif key == 'can':
            base_graph = '''
            +----------------------------+----------------------------+----------------------------+
            | {0[0][0][can]:^9}{0[0][1][can]:^9}{0[0][2][can]:^9}| {0[0][3][can]:^9}{0[0][4][can]:^9}{0[0][5][can]:^9}| {0[0][6][can]:^9}{0[0][7][can]:^9}{0[0][8][can]:^9}|
            | {0[1][0][can]:^9}{0[1][1][can]:^9}{0[1][2][can]:^9}| {0[1][3][can]:^9}{0[1][4][can]:^9}{0[1][5][can]:^9}| {0[1][6][can]:^9}{0[1][7][can]:^9}{0[1][8][can]:^9}|
            | {0[2][0][can]:^9}{0[2][1][can]:^9}{0[2][2][can]:^9}| {0[2][3][can]:^9}{0[2][4][can]:^9}{0[2][5][can]:^9}| {0[2][6][can]:^9}{0[2][7][can]:^9}{0[2][8][can]:^9}|
            +----------------------------+----------------------------+----------------------------+
            | {0[3][0][can]:^9}{0[3][1][can]:^9}{0[3][2][can]:^9}| {0[3][3][can]:^9}{0[3][4][can]:^9}{0[3][5][can]:^9}| {0[3][6][can]:^9}{0[3][7][can]:^9}{0[3][8][can]:^9}|
            | {0[4][0][can]:^9}{0[4][1][can]:^9}{0[4][2][can]:^9}| {0[4][3][can]:^9}{0[4][4][can]:^9}{0[4][5][can]:^9}| {0[4][6][can]:^9}{0[4][7][can]:^9}{0[4][8][can]:^9}|
            | {0[5][0][can]:^9}{0[5][1][can]:^9}{0[5][2][can]:^9}| {0[5][3][can]:^9}{0[5][4][can]:^9}{0[5][5][can]:^9}| {0[5][6][can]:^9}{0[5][7][can]:^9}{0[5][8][can]:^9}|
            +----------------------------+----------------------------+----------------------------+
            | {0[6][0][can]:^9}{0[6][1][can]:^9}{0[6][2][can]:^9}| {0[6][3][can]:^9}{0[6][4][can]:^9}{0[6][5][can]:^9}| {0[6][6][can]:^9}{0[6][7][can]:^9}{0[6][8][can]:^9}|
            | {0[7][0][can]:^9}{0[7][1][can]:^9}{0[7][2][can]:^9}| {0[7][3][can]:^9}{0[7][4][can]:^9}{0[7][5][can]:^9}| {0[7][6][can]:^9}{0[7][7][can]:^9}{0[7][8][can]:^9}|
            | {0[8][0][can]:^9}{0[8][1][can]:^9}{0[8][2][can]:^9}| {0[8][3][can]:^9}{0[8][4][can]:^9}{0[8][5][can]:^9}| {0[8][6][can]:^9}{0[8][7][can]:^9}{0[8][8][can]:^9}|
            +----------------------------+----------------------------+----------------------------+'''
        base_graph = base_graph.format(self.l)
        print(base_graph)

    def fill_candidates(self):
        """填充所有候选数字"""
        for row in range(9):
            for col in range(9):
                unit = self.l[row][col]
                s = set()
                if unit['num'] is '·':
                    s.update([u['num'] for u in self.get_list_of('box', unit['box'])])
                    s.update([u['num'] for u in self.l[row]])
                    s.update([u['num'] for u in self.get_list_of('col', unit['col'])])
                    s.remove('·')
                    s = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} - s
                    unit['can'] = ''.join(sorted(list(s)))
        print('{:^100}'.format('*** 潜在数字填写完毕 ***'), end='')
        self.show()

    def fill_number(self):
        """计算数字并填充"""
        compare_list = copy.deepcopy(self.l)
        while True:
            self.method_saokan()
            if (compare_list == self.l):
                print('{:^100}'.format('*** 扫看循环结束 ***'), end='')
                break
            else:
                compare_list = copy.deepcopy(self.l)

    def method_saokan(self):
        """扫看：候选数字在当前宫唯一，则此格为此数"""
        for box in self.get_list_of('boxes'):
            for unit in box:
                if len(unit['can']) == 1:
                    the_one = unit['can']
                    # 填入数字，删除同行同列的相同候选数字
                    unit['num'] = unit['can']
                    unit['can'] = '[{}]'.format(unit['can'])
                    for u in self.get_list_of('row', unit['row']):
                        u['can'] = u['can'].strip(the_one)
                    for u in self.get_list_of('col', unit['col']):
                        u['can'] = u['can'].strip(the_one)
        print('{:^100}'.format('*** 第 {} 次扫看完毕 ***'.format(self.saokan_count)), end='')
        self.saokan_count += 1
        self.show()


sudoku = Sudoku()

sudoku.start()
