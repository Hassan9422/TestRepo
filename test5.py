#
matrix = [[0 for i in range(4)] for j in range(4)]
matrix[0][0] = 1
matrix[0][2] = 3
matrix[2][1] = 0
matrix[1][3] = 4
matrix[3][3] = 2
matrix[3][0] = 6
for row in matrix:
    print(row)
# print(matrix[2].count(0))
#
# columns = []
# for j in range(4):
#     columns.append([matrix[i][j] for i in range(4)])
#
# for column in columns:
#     print(column)
#
# print(columns[0])
# # for row in matrix:
# #     print(row)
# for e_1, e_2 in [2, 5, 8, 0]:
#     if e_1 == e_2:
#         print('salam')
# l = [0, 1, 1, 3, 4, 5]
# print(l[0:3].count(1))
# import random
#
# for i, element in enumerate(['sdv', 'gmgh', 'ytjyt']):
#     print(element)
# x, y = random.randint(0,3)
# print(x, y)
print('\n')
# columns = [[matrix[i][j] for i in range(4)] for j in range(4)]

list1 = ['a', 'b', 'c']
for i in enumerate(list1):
    print(i[1])
list2 = [0 for n in range(0)]
print(list2)