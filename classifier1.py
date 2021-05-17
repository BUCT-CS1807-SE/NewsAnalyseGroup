# author
#    赵云启
# update:
#       时间    姓名   行为
#    2021-5-13 赵云启 支持正面新闻与负面新闻的分类
#
import json

import requests

API_key = 'ZN5tE3ip0EIIBMRZNoEDhbIR'
Secret_Key = 'pY3QzA7kLEtQQXBAVj0GMmoHssu8u3mG'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_key + '&client_secret=' + Secret_Key
API_URL1 = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_cls/classifier_one'
API_URL2 = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_cls/classifier_two'


class_name1 = {
    '1': '正面新闻',
    '0': '负面新闻',
}


class_name2 = {
    '1': '艺术',
    '2': '文化',
    '3': '科技',
    '4': '娱乐',
    '5': '其他',
}



def get_token():
    response = requests.get(host)
    #
    if response:
        return response.json()['access_token']
    else:
        return "ERROR"


token = get_token()


def get_label2(text):
    headers = {'Content-Type': 'application/json'}
    access_token = token
    # print(access_token)
    params = {"text": text
              }
    ret = requests.post(API_URL2 + "?access_token=" + access_token, headers=headers,
                        data=json.dumps(params).encode('utf-8'), verify=False)
    # print(text)
    # print(ret.json())
    return class_name2[ret.json()['results'][0]['name']]


def get_label1(text):
    headers = {'Content-Type': 'application/json'}
    access_token = token
    # print(access_token)
    params = {"text": text
              }
    ret = requests.post(API_URL1 + "?access_token=" + access_token, headers=headers,
                        data=json.dumps(params).encode('utf-8'), verify=False)
    # print(text)
    print(ret.json())
    return class_name1[ret.json()['results'][0]['name']]


if __name__ == '__main__':
    print(get_label1("筑牢消防安全“防火墙” 我院举办“安全月”系列活动"))
    print(get_label1("人民日报刊文：重新定义博物馆"))
    print(get_label1("“爱国者杯”首届中国文化遗产动漫作品大赛落幕"))
    print(get_label1("网上非法文物贸易猖獗 大英博物馆吁修改法律"))
    print(get_label1("进击的大秦:以“鲜”撬开博物馆，历史穿越时空“活”起来"))
    print(get_label1("博物馆的未来:寻找与公众的结合点"))
    print(get_label1("北京文博|【博物馆之城】走进中国园林博物馆感受园林文化的魅力"))
