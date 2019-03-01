import re
from collections import Counter
import copy
import logging
import time

logging.basicConfig(level=logging.INFO)


class Sudoku:
    def __init__(self):
        # 填写数字的次数
        self.fill_count = 0
        # 循环中方法运行的次数
        self.method_count = 0
        # 保存状态
        self.saved_list = []
        self.saved_number = []

    def start(self):
        # 数独二维数组
        self.l = self.init_suduku_list()
        # 保存一份初始数组，供完成后对照
        self.initial_list = copy.deepcopy(self.l)

        # start!
        self.show('num')
        self.fill_candidates()
        self.method_main()

    def init_suduku_list(self):
        """创建初始的数独组合：二维数组"""
        input_l = []
        print("请逐行输入数独内容，空白格用空格键代替，输入「A」初始化默认初级数独，输入「S」初始化默认最难数独，直接回车初始化默认高级数独")
        i = 1
        while i <= 9:
            num = input('请输入第 {} 行的内容：'.format(i))
            if num == 'a' or num == 'A':
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
            elif num == 's' or num == 'S':
                input_l = ['8········',
                           '··36·····',
                           '·7··9·2··',
                           '·5···7···',
                           '····457··',
                           '···1···3·',
                           '··1····68',
                           '··85···1·',
                           '·9····4··']
                break
            elif num == '':
                input_l = ['·6·3····1',
                           '9····67··',
                           '4·3····2·',
                           '5·98·····',
                           '··45·73··',
                           '·····36·8',
                           '·4····8·3',
                           '··12····7',
                           '3····8·4·']
                break
            elif re.match(r'[1-9(\s)]{9}', num) and len(num) == 9:
                input_l.append(num.replace(' ', '·'))
                i += 1
            else:
                continue
        self._start_time = time.time()
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
        # num: 初始数字及后期已算出确定的数字，str
        # can: candidates，候选数字，如果已确定数字则显示为[1]这种格式，方便调试，str
        # box: 所在宫 row: 所在行 col: 所在列，int
        for i, row in enumerate(input_l):
            for j, unit in enumerate(row):
                input_l[i][j] = {'num': unit,
                                 'can': '[{}]'.format(unit) if unit is not '·' else None,
                                 'box': (i // 3) * 3 + (j // 3),
                                 'row': i,
                                 'col': j}
        return input_l

    def get_list_of(self, key, number=None):
        """拿取宫、行、列的列表"""
        if key == 'boxes':
            # 返回包含 9 个宫的二维数组，每一组是一宫
            boxes = []
            for i in range(9):
                boxes.append([unit for row_list in self.l for unit in row_list if unit['box'] == i])
            return boxes
        elif key == 'num' or key == 'can':
            # 返回全部数字，或候选数字的列表
            return [self.l[row][col][key] for row in range(9) for col in range(9)]
        else:
            # 返回单一宫、行、列的列表
            return [unit for row_list in self.l for unit in row_list if unit[key] == number]

    def show(self, key, desc=None, l=None):
        if l == None:
            l = self.l
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
        base_graph = base_graph.format(l)
        if desc is not None:
            print('{:^100}'.format('*** {} ***'.format(desc)), end='')
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
        self.show('can', '候选数字填写完毕')

    def method_main(self):
        """计算数字并填充"""
        # 无限循环方法1会失效，无限循环方法2会失效
        # 方法1的变动可能会让方法2找到出路，反之相同
        # 交替循环两种方法，能直接解出初级数独，或解出高级数独的大部分内容
        compare_list = copy.deepcopy(self.l)
        while True:
            self.method_paichu()
            self.method_saokan()
            if (compare_list == self.l):
                self.show('num', '循环结束 共计填入过 {} 次'.format(self.fill_count), l=self.initial_list)
                self.show('num')
                break
            else:
                compare_list = copy.deepcopy(self.l)

        # 判断是否已解出数独
        if self.is_valid() and self.get_list_of('num').count('·') == 0:
            print('数独已全解')
            self._end_time = time.time()
            self.interval_time = self._end_time - self._start_time
            return
        else:
            print('高级数独，未全解，启动递归。。。')
            # 判断合法
            if self.is_valid() and self.get_list_of('can').count('') == 0:
                # 合法，开始/继续下一个格子
                # 填入数字
                exit_flag = False
                for row in range(9):
                    for col in range(9):
                        if len(self.l[row][col]['can']) == 2:
                            # 保存状态
                            self.saved_list.append(copy.deepcopy(self.l))
                            self.saved_number.append([row, col, self.l[row][col]['can'][1]])
                            # 填入数字
                            self.fill_number(self.l[row][col], self.l[row][col]['can'][0])
                            exit_flag = True
                            break
                    if exit_flag:
                        break
            else:
                # 不合法，返回上一次状态，填入另一个数字
                self.l = copy.deepcopy(self.saved_list.pop())
                _ = self.saved_number.pop()
                self.fill_number(self.l[_[0]][_[1]], _[2])
                self.show('can', desc='递归测试数字失败，填入另一个数字')
            # 循环方法
            self.method_main()

    def is_valid(self):
        """判断数独是否合法（填错数字也可能合法，要到后面再多填一些数字才能看出来）"""
        for row in range(9):
            for col in range(9):
                unit = self.l[row][col]
                row_list = self.get_list_of('row', row)
                col_list = self.get_list_of('col', col)
                box_list = self.get_list_of('box', unit['box'])
                if row_list.count(unit['num']) > 1:
                    return False
                if col_list.count(unit['num']) > 1:
                    return False
                if box_list.count(unit['num']) > 1:
                    return False
        return True

    def method_paichu(self):
        """排除：当前格只有一个候选数字，则此格为此数"""
        count = 0
        for row in range(9):
            for col in range(9):
                unit = self.l[row][col]
                if len(unit['can']) == 1:
                    self.fill_number(unit, unit['can'])
                    count += 1
                    self.fill_count += 1
        self.method_count += 1
        self.show('can', desc='第 {} 次排除完毕，本次填充了 {} 个数字'.format(self.method_count, count))

    def method_saokan(self):
        """扫看：候选数字在当前宫唯一，则此格为此数"""
        count = 0
        for box in self.get_list_of('boxes'):
            # 先得到只出现一次的数字
            l = []
            for unit in box:
                if '[' not in unit['can']:
                    l.extend(unit['can'])
            # 存入列表，因为每个宫可能有不止一个
            only_one_list = [k for k, v in Counter(l).items() if v == 1]

            for unit in box:
                for the_one in only_one_list:
                    if the_one in unit['can']:
                        # 填入数字，删除同行同列的相同候选数字
                        self.fill_number(unit, the_one)
                        count += 1
                        self.fill_count += 1

        self.method_count += 1
        self.show('can', '第 {} 次扫看完毕，本次填充了 {} 个数字'.format(self.method_count, count))

    def fill_number(self, unit, num):
        """1.填充数字 2.删除同宫、行、列的相同候选数字"""
        unit['num'] = num
        unit['can'] = '[{}]'.format(num)
        for u in self.get_list_of('box', unit['box']):
            if '[' not in u['can'] and num in u['can']:
                u['can'] = u['can'].replace(num, '')
        for u in self.get_list_of('row', unit['row']):
            if '[' not in u['can'] and num in u['can']:
                u['can'] = u['can'].replace(num, '')
        for u in self.get_list_of('col', unit['col']):
            if '[' not in u['can'] and num in u['can']:
                u['can'] = u['can'].replace(num, '')


sudoku = Sudoku()
sudoku.start()
print('共计用时 {} 毫秒'.format(sudoku.interval_time * 1000))
