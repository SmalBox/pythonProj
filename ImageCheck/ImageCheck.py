# ImageCheck

'图像查重，将扫描sourceDir中所有图片，提取出不重复的图片到TargetDir目录中'

__author__ = 'SmalBox'


import os
import shutil
from PIL import Image

# 源目录
sourceDir = './A'
# 目标目录
targetDir = './B'

print('==开始 图像查重==')

### Start

# 文件对比函数_ImgContrast(sourceImg, targetImg), 返回两个图片是否相同的bool值
def _ImgContrast(sourceImg, targetImg):
    # 两个图像对比***
    pass

# 获取源目录下文件名列表，存入sourceList
sourceList = [d for d in os.listdir(sourceDir)]

# 创建目标目录
if not os.path.exists(targetDir):
    os.mkdir(targetDir)

# 遍历源目录，将不重复的文件存入目标目录中
for sourceFile in sourceList:
    # 获取目标目录下文件名列表，存入targetList
    targetList = [d for d in os.listdir(targetDir)]
    # 遍历目标目录下所有文件，与源中取出的文件进行对比
    for targetFile in targetList:
        # sourceFile与targetFile对比
        if _ImgContrast(sourceFile, targetFile):
            break
        else:
            # sourceFile 复制到 targetDir目标目录下
            shutil.copy(sourceDir + sourceFile, targetDir)
            break

### End

print('==图像查重 结束==')
