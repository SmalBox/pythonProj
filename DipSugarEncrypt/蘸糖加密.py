import getpass
import os.path

filePath = input("输入文件路径:")
key = getpass.getpass("输入密钥:")
key = int(key)

outPath = os.path.dirname(filePath)
fileName = os.path.basename(filePath)
newFileName = "Out_" + fileName
outFullPath = os.path.join(outPath, newFileName)

with open(filePath, "rb") as infile, open(outFullPath, "wb") as outfile:
    # 读取待加密文件的数据
    data = infile.read()

    # 转换为字节数组
    data = bytearray(data)

    # 对文件进行异或加密
    maxLength = 512
    for i in range(0, len(data), 4):
        if i < maxLength:
            temp = []
            temp.append(data[i])
            if i + 1 < len(data):
                temp.append(data[i + 1])
            if i + 2 < len(data):
                temp.append(data[i + 2])
            if i + 3 < len(data):
                temp.append(data[i + 3])
            value = int.from_bytes(temp, "little")
            encryptedValue = value ^ key
            encrypted_data = encryptedValue.to_bytes(4, "little")
            data[i] = encrypted_data[0]
            if i + 1 < len(data):
                data[i + 1] = encrypted_data[1]
            if i + 2 < len(data):
                data[i + 2] = encrypted_data[2]
            if i + 3 < len(data):
                data[i + 3] = encrypted_data[3]
        else:
            #data[i] = data[i] ^ 255
            pass

    # 将加密后的数据写入保存文件
    outfile.write(data)

print("完成,输出到：" + outFullPath)
input("按任意键退出……")