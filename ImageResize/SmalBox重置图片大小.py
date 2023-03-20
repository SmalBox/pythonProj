from PIL import Image
import os
import glob

print("==========>SmalBox重置图片大小<==========")
print(">将要处理的图片(.png)放入\"输入\"文件夹中<")
path = r'输入/*.png'
imgWidth = input("输入宽(默认512,按回车保持默认):")
imgHeight = input("输入高(默认512,按回车保持默认):")
if imgWidth == "":
    imgWidth = 512
if imgHeight == "":
    imgHeight = 512
for i in glob.glob(path):
    im1 = Image.open(i)
    im2 = im1.resize((imgWidth,imgHeight))
    im2.save(os.path.join('输出',os.path.basename(i)))
    print('正在生成 Making……：',i)
print('完成 Finish (在输出文件夹查看输出结果。)')
input("按任意键退出……")