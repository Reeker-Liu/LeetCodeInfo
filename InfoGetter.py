import re
import requests


def get_info(id, is_cn = False):
    if is_cn:
        response = requests.get('https://leetcode-cn.com/' + id)
    else:
        response = requests.get('https://leetcode.com/' + id)
    items = re.findall(r'progress-bar-success.*?</span>', response.text, re.S)
    if len(items) == 0:
        return None

    items = [i[22:-8].strip() for i in items]
    # print(items)

    temp = []
    for item in items:
        if item.count("/") > 0:
            temp.append(item)
    items = temp
    # print(items)

    items = items[-2:]

    sq, aq = str.split(items[0], '/')
    sq = int(sq)
    acsub, allsub = str.split(items[1], '/')
    # info = {
    #         'id': id,
    #         'SQ': sq,
    #         'AcSub': acsub,
    #         'AllSub': allsub,
    #         }
    info = [id, sq]
    return info

if __name__ == '__main__':
    print(get_info("we98"))
    print(get_info("huaji"))
    print(get_info("dreamland", True))
    print(get_info("613", True))

