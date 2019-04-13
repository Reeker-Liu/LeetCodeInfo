import  poplib
import DBManager
import MailSender
import InfoHandler
from email.parser import BytesParser
from email.policy import default


def check_mail():
    try:
        fetch_mail()
    except Exception as e:
        print("log error")
        print(e)
        MailSender.send("934422900@qq.com", 'ERROR', "log error\n" + str(e), False)


def fetch_mail():
    # 输入邮件地址, 口令和POP3服务器地址:
    mail_user = "leetcodegroup@qq.com"
    mail_pass = "uhkogqwtiuwrdihj"
    conn = poplib.POP3_SSL('pop.qq.com', 995)
    # 可以打开或关闭调试信息:
    conn.set_debuglevel(0)
    conn.user(mail_user)
    conn.pass_(mail_pass)
    # 获取邮件统计信息，邮件数 总大小
    message_num, total_size = conn.stat()
    if message_num == 0:
        print("no mail found")
        return
    # resp保存服务器的响应码
    # mails列表保存每封邮件的编号、大小
    # resp, mails, octets = conn.list()
    for i in range(message_num):
        # resp保存服务器的响应码, data保存该邮件的内容
        resp, data, octets = conn.retr(i+1)
        # 将字符串内容解析成邮件
        msg_data = b'\r\n'.join(data)
        msg = BytesParser(policy=default).parsebytes(msg_data)
        sender = msg['from'].addresses[0].username + '@' + msg['from'].addresses[0].domain
        subject = msg['subject']
        print("new mail (" + sender + ", " + subject + ")")
        try:
            handle_mail(sender, subject)
        except Exception as e:
            print("handle mail error")
            print(e)
            MailSender.send("934422900@qq.com", 'ERROR', "handle mail error\n" + str(e), False)
    for i in range(message_num):
        conn.dele(i+1)
    conn.quit()
    return


def handle_mail(sender, subject):
    elements =  str.split(subject, ' ')
    if elements[0] not in ["DY", "TD", "CX"]:
        return
    print("handle mail - " + subject + " from " + sender)
    if elements[0] == "DY":
        if len(elements) == 2:
            DBManager.logon_user(elements[1], sender, 0, 0)
        elif len(elements) == 3 and elements[2] == "cn":
            DBManager.logon_user(elements[1], sender, 0, 1)
        else:
            DBManager.logon_user(elements[0], sender, 1)
        MailSender.send(sender, 'Reply to DY', 'register successfully', False)
    elif elements[0] == "TD":
        DBManager.logoff_user(sender)
        MailSender.send(sender, 'Reply to TD', 'quit successfully', False)
    elif elements[0] == "CX":
        DBManager.update_today()
        content = InfoHandler.pack_daily_content()
        MailSender.send(sender, 'Reply to CX', content, True)
    return


if __name__ == '__main__':
    check_mail()
    # subject = "TD