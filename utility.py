base_graph = '''+------+-------+------+
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
+------+-------+------+
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
+------+-------+------+
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
|%s %s %s | %s %s %s | %s %s %s|
+------+-------+------+'''

base_graph = '''+------+-------+------+
|A1 B1 C1 | D1 E1 F1 | G1 H1 I1|
|A2 B2 C2 | D2 E2 F2 | G2 H2 I2|
|A3 B3 C3 | D3 E3 F3 | G3 H3 I3|
+------+-------+------+
|A4 B4 C4 | D4 E4 F4 | G4 H4 I4|
|A5 B5 C5 | D5 E5 F5 | G5 H5 I5|
|A6 B6 C6 | D6 E6 F6 | G6 H6 I6|
+------+-------+------+
|A7 B7 C7 | D7 E7 F7 | G7 H7 I7|
|A8 B8 C8 | D8 E8 F8 | G8 H8 I8|
|A9 B9 C9 | D9 E9 F9 | G9 H9 I9|
+------+-------+------+'''


default_list1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 3, 4, 5, 6, 7, 8]]

default_list2 = [[1, 0, 6, 2, 0, 0, 0, 0, 0],
                 [0, 0, 0, 4, 0, 0, 8, 2, 0],
                 [2, 0, 0, 0, 0, 5, 0, 0, 0],
                 [0, 8, 0, 0, 4, 0, 0, 0, 7],
                 [0, 0, 0, 6, 0, 3, 0, 0, 0],
                 [5, 0, 0, 0, 1, 0, 0, 4, 0],
                 [0, 0, 0, 9, 0, 0, 0, 0, 0],
                 [0, 3, 9, 0, 0, 4, 0, 0, 0],
                 [0, 0, 0, 0, 0, 2, 9, 0, 5]]

l = ['  18 9 6 ', '259  34  ', '4 8 251  ', '84 3  62 ', '  768  95', ' 9  7   1', ' 1623  5 ', ' 7  1 2  ',
                 '3  4 7   ']

# for row in 'abcdefghi':
#     for col in '123456789':
#         # 判断空格
#         unit = self.__getattr__(row + col)
#         s = []
#         if unit['num'] is '·':
#             # 统计宫
#             for u in self.box[unit['box']]:
#                 pass#s.append(u['num'])
#             # 统计行
#             for i in range(1, 10):
#                 u = self.__getattr__(row + str(i))
#                 s.append(u['num'])
#             # 统计列
#             print(s)
