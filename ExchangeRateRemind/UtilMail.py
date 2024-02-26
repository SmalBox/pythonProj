import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 设置邮箱账号和密码
email = 'from@163.com'
password = 'AuthorizationCode'

# 设置收件人邮箱
receiver_email = 'to@gmail.com'

def send_email(title:str, content:str):
    # 创建邮件内容
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = email
    message['To'] = receiver_email
    message['Subject'] = Header(title, 'utf-8')

    # 连接到SMTP服务器并发送邮件
    print('==>连接邮箱服务器…')
    server = smtplib.SMTP('smtp.163.com', 25)  # 请替换为你的SMTP服务器地址和端口
    print('==>设置加密')
    server.starttls()  # 使用TLS加密通信
    print('==>登录邮箱')
    server.login(email, password)
    print('==>发送邮件')
    server.sendmail(email, receiver_email, message.as_string())
    server.quit()

    print('%s 邮件发送成功！' % receiver_email)