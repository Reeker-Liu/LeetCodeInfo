import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart


def send(receivers, subject, content, is_html):
    mail_user="leetcodegroup@qq.com"
    mail_pass="uhkogqwtiuwrdihj"
    sender = 'leetcodegroup@qq.com'

    if is_html:
        message = MIMEMultipart()
        message.attach(MIMEText(content, 'html', 'utf-8'))
    else:
        message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(["leetcode交流群通知", sender])
    message['To'] = Header('交流群成员', 'utf-8')
    message['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        print("send email done")
    except smtplib.SMTPException as e:
        print(e)



if __name__ == '__main__':
    body = '''1'''
    send(["934422900@qq.com"], "!23", body, True)
    print("done")