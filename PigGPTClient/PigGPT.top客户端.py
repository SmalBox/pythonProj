#coding=utf-8
import json
import requests
import os
import glob
import time

# region V1.1.0 当前版本
# 支持单行、多行提问模式切换功能。
# 使用 "pigpig" 命令切换两种模式。
# 多行模式下 使用 "nono" 命令可以重写上一行内容。
# 多行模式下 使用 "nonono" 命令可以重写本次提问内容。
# endregion

# region V1.0.1 当前版本
# 增强请求发送时的异常捕获，自动重发。
# endregion

# region V1.0.0 版本需求
# 本地数据从当前文件夹的 PigGPT.top.Data 取
# 每段对话为一个json存储在上述文件夹中
# 程序开始会搜索本地数据文件夹中的内容，以便从之前的会话中继续会话
# 用户可以根据列出的序号选择继续哪段对话（0为新的对话）
# 新的对话会让用户为此会话起名字，json会以此作为名字存储
# 非新对话时，会根据之前内容，将之前的所有问答打印出来
# json会按顺序存储问的问题，和所有返回的答案
# 用户根据提示输入问题，程序将此会话之前的内容取出加上最新的问题，发送给PigGPT
# 当返回内容时，解析最新的内容显示在屏幕上，并将此次问题和返回的内容记录到json中
# endregion


# region 启动提示
print("\n\n")
print("==> 我是 PigGPT V1.0.0 <==")
print("==> (・ω・)我有记忆力,我会结合当前会话的所有内容与你交谈 <==")
print("==> (・ω・) 输入 “886” 结束对话 <==")
print("\n")
# endregion

# region 启动设置配置
# 请求的URL
url = "http://smalbox.top/PigGPT"
dataPath = "./PigGPT.top.Data/"

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 读取配置
with open("./PigGPT.top.Config/Config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    url = config["url"]
    dataPath = config["dataPath"]
# endregion

# region 获取本地数据内容
dataPathMatch = os.path.join(dataPath, "*.json")
passageNames = []
print("0.创建新会话")
passageIndex = 1
for name in glob.glob(dataPathMatch):
    passageNames.append(name)
    print(str(passageIndex) + "." + os.path.basename(name))
    passageIndex += 1
print("\n")

# endregion

# region 选择会话
selectedPassageIndex = input("输入序号选择会话(输入q退出)：")
while True:
    try:
        # q退出程序
        if selectedPassageIndex.lower() == "q":
            break
        isError = int(selectedPassageIndex) < 0 or \
            int(selectedPassageIndex) > len(passageNames)
        if isError:
            selectedPassageIndex = input("输入序号选择会话(输入q退出)：")
        else:
            break
    except:
        selectedPassageIndex = input("输入序号选择会话(输入q退出)：")
        continue
# endregion

class InputModel():
    SingleLine = 0
    MultiLine = 1

# q退出程序
if selectedPassageIndex.lower() != "q":
    if int(selectedPassageIndex) == 0: # 创建新对话
    # region 手动起名阶段(后续会替换成gpt总结第1轮对话自动起名)
        passageName = input("此段对话的主题：")
        passageFilePath = os.path.join(dataPath, passageName + ".json")
    # endregion
    else:
    # region 显示内容阶段,将之前的会话记录展示出来
        passageFilePath = passageNames[int(selectedPassageIndex) - 1]
        try:
            with open(passageFilePath, "r", encoding="utf-8") as f:
                content = json.load(f)
            for round in content:
                userContent = round["user"]
                pigGPTContent = round["pigGPTContent"]
                print("====> User: <====")
                print(userContent["content"] + "\n")
                print("====> PigGPT: <====")
                print(pigGPTContent["choices"][0]["message"]["content"] + "\n")
        except:
            pass
    # endregion

    # region 输入循环
    inputModel:InputModel = InputModel.SingleLine
    inputQuestion = ""
    while True:
        # 数据输入
        # 输入类型判断
        while True:
            try:
                inputQuestion = ""
                if inputModel == InputModel.SingleLine:
                    inputQuestion = input("(单)对PigGPT(・ω・)说(输入pigpig切换多行模式)：")
                    if inputQuestion == "":
                        print("啥也没说的(´･ω･`)?\n")
                        continue
                    if inputQuestion == "886":
                        print("\n==> 886 (・ω・) Bye~ <==\n")
                        input("按任意键退出……")
                        break
                    if inputQuestion.lower() == "pigpig":
                        inputModel = InputModel.MultiLine
                        print("\n==> 开启多行输入 (・ω・) Yeah~ <==\n")
                        continue
                    break
                elif inputModel == InputModel.MultiLine:
                    print("输入pigpig切换单行模式;结尾行输入okok提交多行内容;")
                    print("输入nono重写上一行;输入nonono重新输入本段.")
                    inputText = input("(多)对PigGPT(・ω・)说：\n")
                    if inputText == "886":
                        inputQuestion += inputText
                        print("\n==> 886 (・ω・) Bye~ <==\n")
                        input("按任意键退出……")
                        break
                    if inputText.lower() == "pigpig":
                        inputModel = InputModel.SingleLine
                        print("\n==> 开启单行输入 (・ω・) Yeah~ <==\n")
                        continue
                    if inputText.lower() == "okok" or \
                        inputText.lower() == "nono" or \
                        inputText.lower() == "nonono":
                        print("啥也没说的(´･ω･`)?\n")
                        continue
                    inputQuestion += inputText
                    while True:
                        try:
                            inputText = input()
                            if inputText.lower() == "nono": # 重写单行输入
                                print("重新输入上一行内容：\n")
                                continue
                            if inputText.lower() == "nonono": # 重写多行输入
                                inputQuestion = inputText
                                break
                            if inputText.lower() == "okok": # 结束多行输入
                                break
                            inputQuestion += inputText
                        except:
                            break
                    if inputQuestion.lower() == "nonono":
                        print("重写本段:\n")
                        continue
                    else:
                        break
                else:
                    print("啥也没说的(´･ω･`)?\n")
            except:
                print("有异常 再说一遍呗(´･ω･`)!\n")
                continue
        if inputQuestion == "886":
            break

        print("==> 我在思考~ 等我一下组织语言~ (・ω・) En… <==")

        # 准备对话数据数组
        # 取json中本会话之前的数据
        lastMessage = []
        if os.path.exists(passageFilePath):
            try:
                with open(passageFilePath, "r", encoding="utf-8") as f:
                    content = json.load(f)
                for round in content:
                    userContent = round["user"]
                    pigGPTContent = round["pigGPTContent"]["choices"][0]["message"]
                    lastMessage.append(userContent)
                    lastMessage.append(pigGPTContent)
            except:
                pass
        # 组装好本次数据
        curMessage = {"role":"user", "content": inputQuestion}
        # 拼装好对话数组
        lastMessage.append(curMessage)
        json.dumps(lastMessage)
        messages = lastMessage

        # JSON数据
        data = {
            "token": "",
            "model": "",
            "messages": messages
        }

        # 将字典转换为JSON格式的字符串
        json_data = json.dumps(data)

        while True:
            requestTimes = 0
            try:
                # 使用POST方法发送JSON请求
                response = requests.post(url, data=json_data, headers=headers)
                # 检查响应状态码
                if response.status_code == 200:
                    if os.path.exists(passageFilePath):
                        try:
                            with open(passageFilePath, "r", encoding="utf-8") as f:
                                content = json.load(f)
                        except:
                            content = []
                    else:
                        content = []
                    # 本地存储
                    with open(passageFilePath, "w", encoding="utf-8") as f:
                        # 本次会话请求、本次会话返回 添加存入本地数据
                        newElement = {"user": curMessage, "pigGPTContent": response.json()}
                        content.append(newElement)
                        #newDataStr = json.dumps(newContent)
                        #json.dump(json.loads(newDataStr), f, indent=4, ensure_ascii=False)
                        json.dump(content, f, indent=4, ensure_ascii=False)

                    # 打印显示
                    print("\n")
                    print("PigGPT(・ω・)说：\n", response.json()["choices"][0]["message"]["content"])
                    print("\n")
                    break
                else:
                    print("请求失败！")
                    print("状态码：", response.status_code)
                    print("响应内容：", response.text)
                    print("请检查网络，或重启程序，实在不行请联系 人工GPT (・ω・)\n")
                    input("按任意键继续……")
                    break
            except Exception as e:
                if requestTimes < 3:
                    time.sleep(5)
                    print(e)
                    print("\n请求异常，正在重新请求。 请稍后……")
                    requestTimes += 1
                    continue
                else:
                    print("请检查网络，或重启程序，实在不行请联系 人工GPT (・ω・)\n")
                    input("按任意键继续……")
                    break
    # endregion