#coding=utf-8
import json
import requests

# V1.0.0 版本需求
# 本地数据从当前文件夹的 PigGPT.top.Data 取
# 每段对话为一个json存储在上述文件夹中
# 程序开始会搜索本地数据文件夹中的内容，以便从之前的会话中继续会话
# 用户可以根据列出的序号选择继续哪段对话（0为新的对话）
# 新的对话会让用户为此会话起名字，json会以此作为名字存储
# 非新对话时，会根据之前内容，将之前的所有问答打印出来
# json会按顺序存储问的问题，和所有返回的答案
# 用户根据提示输入问题，程序将此会话之前的内容取出加上最新的问题，发送给PigGPT
# 当返回内容时，解析最新的内容显示在屏幕上，并将此次问题和返回的内容记录到json中

# v0.1.0 版本(当前版本)
# 每次问一个问题，无上下问结合

print("\n\n")
print("==> 我是 PigGPT V0.1.0 <==")
print("==> (・ω・)我没有记忆力,我只记得当下这句话的问题 <==")
print("==> (・ω・) 输入 “886” 结束对话 <==")
print("\n")

# 请求的URL
url = "http://smalbox.top/PigGPT"

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 读取配置
with open("./PigGPT.top.Config/Config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    url = config["url"]

inputQuestion = ""
while inputQuestion != "886":
    # 数据输入
    inputQuestion = input("对PigGPT(・ω・)说：")
    while inputQuestion == "":
        print("啥也没说的(´･ω･`)?\n")
        inputQuestion = input("对PigGPT(・ω・)说：")
    if (inputQuestion == "886"):
        print("\n==> 886 (・ω・) Bye~ <==\n")
        input("按任意键退出……")
        break
    print("==> 我在思考~ 等我一下组织语言~ (・ω・) En… <==")

    # JSON数据
    data = {
        "token": "",
        "model": "",
        "messages": [
            {"role":"user", "content": inputQuestion},
            ]
    }

    # 将字典转换为JSON格式的字符串
    json_data = json.dumps(data)

    # 使用POST方法发送JSON请求
    response = requests.post(url, data=json_data, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        print("\n")
        print("PigGPT(・ω・)说：\n", response.json()["choices"][0]["message"]["content"])
        print("\n")
    else:
        print("请求失败！")
        print("状态码：", response.status_code)
        print("响应内容：", response.text)
        print("请检查网络，或重启程序，实在不行请联系 人工GPT (・ω・)\n")
        input("按任意键退出……")
        break
