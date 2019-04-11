import MailSender
import DBManager


def get_css():
    css = '''
    <style type="text/css">
    table caption{
		padding:5px 0px;
		font-size:20px;
		color:#c00;
	}
    /* gridtable */
    table.gridtable {
        font-family: verdana,arial,sans-serif;
        font-size:11px;
        color:#333333;
        border-width: 1px;
        border-color: #666666;
        border-collapse: collapse;
    }
    table.gridtable th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #dedede;
    }
    table.gridtable td {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #ffffff;
    }
    </style>
    '''
    return css

def pack_table(caption, headers, rows):
    body = '<table class="gridtable" border="1" cellpadding="5">\n'
    body += '<caption>' + caption + '</caption>\n'

    body += '<tr>\n'
    for header in headers:
        body += '<th align="center">'+ header + '</th>\n'
    body += '</tr>\n'

    for row in rows:
        body += '<tr>\n'
        for element in row:
            body += '<td align="right">' + str(element) + '</td>'
        body += '</tr>\n'

    body += '</table>'
    return body

def pack_daily_content(td_ranks, all_ranks, new_users):
    temp_list = []
    rank = 1
    for row in td_ranks:
        temp_list.append([rank] + row)
        rank += 1
    td_ranks = temp_list

    temp_list = []
    rank = 1
    for row in all_ranks:
        temp_list.append([rank] + row)
        rank += 1
    all_ranks = temp_list

    content = get_css()
    headers = ["Rank", "User ID", "Solved"]
    content += pack_table("Today Rank", headers, td_ranks)
    content += '<br><br>'
    content += pack_table("Leaderboard", headers, all_ranks)
    content += '''
    <font size="1" color="gray">
    * users only appear in the Leaderboard if they registered today
    </font>
    '''
    content += '<br><br><br>'
    content += '''
    <font size="1" color="gray">
    - welcome to join our leetcode group 730372043 -
    </font>
    '''
    return content


def get_formatted_info():
    td_ranks = []
    all_ranks = []
    new_users = []
    infos = DBManager.get_data()
    receivers = [info[1] for info in infos]
    for info in infos:
        if not info[4]:
            all_ranks.append([info[0], info[3]])
            if info[2]:
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
    # print(content)
    MailSender.send(receivers, 'Daily LeetCode Notice', content, True)
    print("daily job done")


if __name__ == '__main__':
    daily_job()
    print("done")