# PyReg.py

'Python正则表达式文本替换工具'

__author__ = 'SmalBox'


import os
import io
import re

while True:
    print("{:=^30}".format("Start Regular"))
    # Get File Path and Name, check file exist.
    while True:
        filePath = input("Enter File Path: ")
        if os.path.exists(filePath) == True:
            break
        else:
            print("File not Found, Please enter again!\n")
    pattern = input("Enter Regular: ")
    replacedStr = input("Enter Replaced String: ")

    with io.open(filePath, 'r', encoding="utf-8") as f:
        fileContent = f.read()
        print("{:=^30}".format("File Read Completed"))
        print("\n{:▼^30}".format("File Original Content:"))
        print("{}".format(fileContent))
        print("{:▲^30}\n".format(''))
        replaced = re.subn(pattern, replacedStr, fileContent)
        print("{:▼^30}".format("Replaced result:"))
        print("{}".format(replaced[0]))
        print("{:▲^30}\n".format(''))
        if replaced[1] == 0:
            print("{:=^30}".format("Not Match!"))
        else:
            print("Match {} place!".format(replaced[1]))
            while True:
                isWrite = input("Yes or No Write?\nPlease enter Y or N: ")
                if isWrite == 'Y' or isWrite =='y':
                    fileContent = replaced[0]
                    with io.open(filePath, 'w+', encoding="utf-8") as f:
                        f.write(fileContent)
                        print("{:=^30}".format("Write Completed"))
                    break
                elif isWrite == 'N' or isWrite == 'n':
                    break
                else:
                    print("Please Enter Again Correctly!")
    isExit = input("Yes or No Exit?\nPlease enter Y or N: ")
    if isExit == 'Y' or isExit == 'y':
        break

print("{:=^30}".format("End Regular"))
