import requests
from bs4 import BeautifulSoup

import UtilMail

# 设置邮箱账号和密码
email = 'smal_box@163.com'
password = 'xxx'

# 设置收件人邮箱
receiver_email = 'e1@smalbox.com'
receiver_email2 = 'e2@smalbox.com'

UtilMail.email = email
UtilMail.password = password
UtilMail.receiver_email = receiver_email


## 获取数据

url = 'https://www.boc.cn/sourcedb/whpj/sjmfx_1621.html'
try:
    response = requests.get(url)
except Exception as e:
    print("请求异常")
    print(e)
soup = BeautifulSoup(response.content, 'html.parser')

target_trTitle = None

for trTitle in soup.find_all('tr'):
    if '货币' in trTitle.find('th'):
        target_trTitle = trTitle
        break

if target_trTitle:
    #print(target_trTitle)
    tr_contentTitle = [th.get_text().replace('\n', '').replace(' ', '') for th in trTitle.find_all('th')]
    #print(tr_content)
else:
    print("No <tr> tag with Title found.")

target_tr = None
for tr in soup.find_all('tr'):
    if tr.find('td', string='AED'):
        target_tr = tr
        break

if target_tr:
    #print(target_tr)
    tr_content = [td.get_text() for td in tr.find_all('td')]
    #print(tr_content)
else:
    print("No <tr> tag with <td>AED</td> found.")


## 组织内容 发送邮件
import datetime

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

data = {"Date": formatted_datetime}
content = formatted_datetime + "\n"
for i in range(0, len(tr_contentTitle)):
    content += tr_contentTitle[i] + ": "
    if (i < len(tr_content)):
        content += tr_content[i] + "\n"
        data[tr_contentTitle[i].encode('gbk').decode('gbk')] = tr_content[i]
title = "AED现钞入:%s" % tr_content[2]

print("发送邮件通知今日消息")
UtilMail.send_email(title=title, content=content)
UtilMail.receiver_email = receiver_email2
UtilMail.send_email(title=title, content=content)

print(title)
print(content)


## 数据写入：

import json
# Define the filename based on the current date
filename = f"迪拉姆汇率数据.json"

# Read existing data from the file
try:
    with open(filename, 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

# Update existing data with new data
existing_data.append(data)

# Write the updated data back to the file
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, indent=4, ensure_ascii=False)

print(f"Data has been incrementally stored in {filename}")

input("输入任意退出")