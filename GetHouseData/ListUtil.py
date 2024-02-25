
def chunk(lst, n):
    """
    将列表lst每n个一组切分为多个列表
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# 测试
# lst = [1, 2, 3, 4, 5, 6, 7, 8]
# n = 3
# print(chunk(lst, n))
# 输出：
# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]