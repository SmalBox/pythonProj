import csv
import os

# 创建一个列表
data = [['姓名', '年龄', '性别'],
        ['张三', 20, '男'],
        ['李四', 25, '女']]

# # 将列表中的内容存储为 CSV 格式的文件
# with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     # 创建一个 CSV 写入器
#     csvwriter = csv.writer(csvfile)

#     # 写入列表中的内容
#     csvwriter.writerows(data)

def SaveListToCsv(savePathFullName:str, dataList:list,
                  autoOpenDir:bool = False,
                  encoding:str = "utf-8") -> None:
    with open(savePathFullName, 'w',
              newline='', encoding=encoding) as csvfile:
        # 创建一个 CSV 写入器
        csvwriter = csv.writer(csvfile)

        # 写入列表中的内容
        csvwriter.writerows(dataList)
    # 自动打开目录
    if (autoOpenDir):
        os.system(r'explorer %cd%')

# Open the CSV file
with open('data.csv', 'r', encoding='utf-8') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)

    # Read the header row
    header = next(reader)

    # Read the remaining rows
    rows = list(reader)

# Print the header
print(header)

# Print the first row
print(rows[0])


#SaveListToCsv('data.csv', data, True)