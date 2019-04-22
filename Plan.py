import MailSender
import MailReceiver
import DBManager
import InfoHandler
import schedule
import time


def daily_job():
    DBManager.update_today()
    content = InfoHandler.pack_daily_content()
    receivers = DBManager.get_auditors()
    MailSender.send(receivers, 'Daily LeetCode Notice', content, True)
    DBManager.update_yestoday()
    print("daily job done")
    return


def plan():
    print("scheduling start")
    schedule.every().minute.do(MailReceiver.check_mail)
    schedule.every().day.at("11:20").do(daily_job)
    while True:
        print("try scheduling")
        schedule.run_pending()
        time.sleep(20)

if __name__ == '__main__':
    plan()
    print("done")