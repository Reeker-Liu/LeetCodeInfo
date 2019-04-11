import MailSender
import DBManager
import pandas as pd


def pack_daily_content(td_ranks, all_ranks, new_users):
    content = "========== Today ==========\n"\
              + "  rank  "\
              +"  solved  " \
              + "user id".rjust(18) + "\n"
    for i in range(len(td_ranks)):
        content += str(i+1).rjust(8) \
                   + str(td_ranks[i][1]).rjust(9) \
                   + str(td_ranks[i][0]).rjust(18) + "\n"
    content += "=========================\n\n"

    content += "=========== All ===========\n" \
               + "  rank  " \
               + "  solved  " \
               + "user id".rjust(18) + "\n"
    for i in range(len(all_ranks)):
        content += '{:>8}'.format(i+1) \
                   + '{:>9}'.format(all_ranks[i][1]) \
                   +'{:>18}'.format(all_ranks[i][0]) + "\n"
    content += "=========================\n\n"

    if len(new_users) > 0:
        content += "==== New registered users ====\n"
        content += "    "
        for user in new_users:
            content += user + "   "
        content += "\n"
        content += "=========================\n\n"

    content += "== welcome to join our leetcode group ==\n"\
                  + "=== QQ group number : 730372043 ===\n"

    return content


def pack_daily_content2(td_ranks, all_ranks, new_users):
    #https://blog.csdn.net/xiaosongbk/article/details/60142996
    d = {}
    index = 0
    title = ["1", "2"]
    for t in title:
        d[t] = td_ranks[index]
        index = index + 1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html()
    return h

def get_formatted_info():
    td_ranks = []
    all_ranks = []
    new_users = []
    infos = DBManager.get_data()
    receivers = [info[1] for info in infos]
    for info in infos:
        if not info[4]:
            if info[2]:
                all_ranks.append([info[0], info[3]])
                td_ranks.append([info[0], info[3] - info[2]])
            else:
                new_users.append(info[0])
    td_ranks.sort(key=lambda x:x[1], reverse=True)
    all_ranks.sort(key=lambda x:x[1], reverse=True)
    return  td_ranks, all_ranks, new_users, receivers

def daily_job():
    DBManager.update_yestoday()
    DBManager.update_today()
    td_ranks, all_ranks, new_users, receivers = get_formatted_info()
    content = pack_daily_content(td_ranks, all_ranks, new_users)
    MailSender.send(receivers, content, 'Daily LeetCode Notice')
    print("daily job done")


if __name__ == '__main__':
    # daily_job()
    td_ranks, all_ranks, new_users, receivers = get_formatted_info()
    print(pack_daily_content2(td_ranks, all_ranks, new_users))
    print("done")