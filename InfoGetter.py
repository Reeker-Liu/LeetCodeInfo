import re
import requests


def get_info(id):
    response = requests.get('https://leetcode.com/' + id)
    items = re.findall(r'progress-bar-success.*?</span>', response.text, re.S)
    items = [i[22:-8].strip() for i in items]
    if len(items) == 0:
        return None
    if len(items) == 6:
        items = items[1:3]
    else:
        items = items[3:5]
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
