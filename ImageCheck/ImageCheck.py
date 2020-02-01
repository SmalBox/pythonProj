# ImageCheck

'图像查重，将扫描sourceDir中所有图片，提取出不重复的图片到targetDir目录中'

__author__ = 'SmalBox'


import os
import shutil
import time
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

startTime = time.time()
# 源目录
sourceDir = '.\\A'
# 目标目录
targetDir = '.\\B'

print('==开始 图像查重 start==', flush=True)

### Start

# 获取源目录下图片数据信息
def _GetImageInfo(imageDirPath):
    imgList = [d for d in os.listdir(imageDirPath)]
    imgInfo = list()
    openFailList = list()
    completeNum = 0
    for imgName in imgList:
        try:
            with Image.open(imageDirPath + '\\' + imgName, 'r') as img:
                imgSize = img.size
                img00 = img.getpixel((0, 0))
                imgWidth0 = img.getpixel((imgSize[0] - 1, 0))
                imgWidthHeight = img.getpixel((imgSize[0] - 1, imgSize[1] - 1))
                img0Height = img.getpixel((0, imgSize[1] - 1))
                imgInfo.append({\
                    'name' : imgName,\
                    'size' : imgSize,\
                    'img00' : img00,\
                    'imgWidth0' : imgWidth0,\
                    'imgWidthHeight' : imgWidthHeight,\
                    'img0Height' : img0Height})
        except:
            openFailList.append(imgName)
            print('\nOpen Error！，FileName：%s，成功：%d，失败：%d' % (imgName, len(imgInfo), len(openFailList)), flush=True)
            time.sleep(1)
            continue
        completeNum += 1
        print('\r已完成(CMPE) %d ，进度(PROG)：%.2f%%，%s，imgInfoLen:%d，Time：%.2fs'\
            % (completeNum, \
            completeNum * 100 / len(imgList), \
            imageDirPath + '\\' + imgName, \
            len(imgInfo), \
            (time.time() - startTime)), \
            end='', flush=True)
    print('成功：%d，失败：%d' % (len(imgInfo), len(openFailList)), flush=True)
    print('失败文件：%s' % openFailList)
    return imgInfo


# 文件信息对比函数，对比两个图片信息是否相同
def _ImgInfoContrast(sourceImgInfo, targetImgInfo):
    if sourceImgInfo['size'] == targetImgInfo['size'] and \
    sourceImgInfo['img00'] == targetImgInfo['img00'] and \
    sourceImgInfo['imgWidth0'] == targetImgInfo['imgWidth0'] and \
    sourceImgInfo['imgWidthHeight'] == targetImgInfo['imgWidthHeight'] and \
    sourceImgInfo['img0Height'] == targetImgInfo['img0Height']:
        return True
    else:
        return False

# main:

# 预处理，将源目录中数据加载到内存
print('开始预加载！\n', flush=True)
sourceImgInfo = _GetImageInfo(sourceDir)
num = 5
for i in range(5):
    print('\r预加载完成！ %ds后开始图像查重\n' % num, flush=True)
    num -= 1
    time.sleep(1)

# 创建目标目录
if not os.path.exists(targetDir):
    os.mkdir(targetDir)
    
# 遍历源目录，将不重复的文件存入目标目录中
completeNum = 0

# 创建sizeDict将查过的图片按照尺寸进行分类
sizeDict = { }

for sourceFile in sourceImgInfo:
    targetList = [d for d in os.listdir(targetDir)]  # 获取目标目录下文件名列表，存入targetList
    imgW, imgH = sourceFile['size']  # 获取要比较文件的宽高
    imgSize = str(imgW) + 'x' + str(imgH)

    if len(targetList) == 0:
        # 如果目标文件夹里没有文件，则直接放入
        shutil.copy(sourceDir + '\\' + sourceFile['name'], targetDir)
        # 根据尺寸存入字典
        sizeDict.update({imgSize : [sourceFile]})
        completeNum += 1
        continue

    findCopy = False  # 设置是否找到副本标记
    if imgSize in sizeDict:
        for targetFile in sizeDict[imgSize]:
            print('\r已完成(CMPE) %d ，进度(PROG)：%.2f%%，%s <=> %s，Time：%.2fmin'\
                % (completeNum, \
                completeNum * 100 / len(sourceImgInfo), \
                sourceDir + '\\' + sourceFile['name'], \
                targetDir + '\\' + targetFile['name'], \
                (time.time() - startTime) / 60), \
                end='', flush=True)
            result = _ImgInfoContrast(sourceFile, targetFile)
            if result == -1 or result:
                findCopy = True
                break
        if not findCopy:
            # 如果没有重复副本，则将sourceFile 复制到 targetDir目标目录下
            shutil.copy(sourceDir + '\\' + sourceFile['name'], targetDir)
            # 根据尺寸存入字典
            sizeDict[imgSize].append(sourceFile)
    else:
        # 如果没有同大小的图片，则直接复制，创建新的尺寸分类
        sizeDict.update({imgSize : [sourceFile]})
        shutil.copy(sourceDir + '\\' + sourceFile['name'], targetDir)
    completeNum += 1

### End

print('\n==图像查重 结束 End==', flush=True)
