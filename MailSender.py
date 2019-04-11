import InfoGetter
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

ids = ["we98", "huaji"]
content = ">>>>>>>>>>>>>>>>>>>>>>>>\n"
for id in ids:
    info = InfoGetter.get_info(id)
    for k in info:
        content += k + " : " + info[k] + "\n"
    content += ">>>>>>>>>>>>>>>>>>>>>>>>\n"

mail_host="smtp.qq.com"  #设置服务器
mail_user="leetcodegroup@qq.com"    #用户名
mail_pass="uhkogqwtiuwrdihj"   #口令
sender = 'leetcodegroup@qq.com'
receivers = ['934422900@qq.com']

message = MIMEText(content, 'plain', 'utf-8')
message['From'] = formataddr(["leetcode交流群通知", sender])
# message['To'] = formataddr(["交流群成员",  receivers[0]])
# message['From'] = Header('leetcode交流群通知', 'utf-8')
message['To'] = Header('交流群成员', 'utf-8')
message['Subject'] = 'Daily LeetCode Notice'

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(mail_user, mail_pass)
    server.sendmail(sender, receivers, message.as_string())
    server.quit()
    print("done")
except smtplib.SMTPException as e:
    print(e)
