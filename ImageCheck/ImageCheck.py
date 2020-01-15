# ImageCheck

'图像查重，将扫描sourceDir中所有图片，提取出不重复的图片到targetDir目录中'

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

# 文件对比函数_ImgContrast(sourceImgPath, targetImgPath), 返回两个图片是否相同的bool值
def _ImgContrast(sourceImgPath, targetImgPath):
    # 两个图像对比
    # 打开两个图片
    try:
        sourceImg = Image.open(sourceImgPath, 'r')
        targetImg = Image.open(targetImgPath, 'r')
    except:
        print('\n无法打开文件：%s' % sourceImgPath)
        return -1
    
    # 对比两图片宽高
    if sourceImg.size == targetImg.size:
        width = sourceImg.width - 1
        height = sourceImg.height - 1
        # 对比两图片四角像素(0, 0) (width, 0) (width, height) (0, height)
        if sourceImg.getpixel((0, 0)) == targetImg.getpixel((0, 0)) and\
        sourceImg.getpixel((width, 0)) == targetImg.getpixel((width, 0)) and\
        sourceImg.getpixel((width, height)) == targetImg.getpixel((width, height)) and\
        sourceImg.getpixel((0, height)) == targetImg.getpixel((0, height)):
            # 对比每个像素***
            sourceImg.close()
            targetImg.close()
            return True
        else:
            sourceImg.close()
            targetImg.close()
            return False
    else:
        sourceImg.close()
        targetImg.close()
        return False
    # 返回两图片是否相同

# 获取源目录下文件名列表，存入sourceList
sourceList = [d for d in os.listdir(sourceDir)]

# 创建目标目录
if not os.path.exists(targetDir):
    os.mkdir(targetDir)

# 遍历源目录，将不重复的文件存入目标目录中
completeNum = 0
for sourceFile in sourceList:
    # 获取目标目录下文件名列表，存入targetList
    targetList = [d for d in os.listdir(targetDir)]
    if len(targetList) == 0:
        # 如果目标文件夹里没有文件，则直接放入
        shutil.copy(sourceDir + '\\' + sourceFile, targetDir)
        continue
    # 遍历目标目录下所有文件，与源中取出的文件进行对比
    findCopy = False  # 设置是否找到副本标记
    for targetFile in targetList:
        # sourceFile与targetFile对比
        if _ImgContrast(sourceDir + '\\' + sourceFile, targetDir + '\\' + targetFile) == -1:
            findCopy = True
            break
        if _ImgContrast(sourceDir + '\\' + sourceFile, targetDir + '\\' + targetFile):
            findCopy = True
            break
    if not findCopy:
        # 如果没有重复副本，则将sourceFile 复制到 targetDir目标目录下
        shutil.copy(sourceDir + '\\' + sourceFile, targetDir)

    completeNum += 1
    print('\r已经完成 %d 个，进度：%.2f%%' % (completeNum, completeNum * 100 / len(sourceList)), end='')

### End

print('\n==图像查重 结束==')
