import re
import numpy
from collections import Counter
import copy
import logging
import json

logging.basicConfig(level=logging.INFO)


class Sudoku:
    def __init__(self):
        # 数独二维数组
        self.l = self.init_suduku_list()
        # 保存一份初始数组，供完成后对照
        self.initial_list = copy.deepcopy(self.l)


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

    def get_list_of(self, position, number):
        """拿取整个宫、行、列的列表"""
        return [unit for row_list in self.l for unit in row_list if unit[position] == number]

    def show(self):
        """图形化显示数独二维数组"""
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
        base_graph = base_graph.format(self.l)
        print(base_graph)


sudoku = Sudoku()

sudoku.show()