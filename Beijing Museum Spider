# -*- coding:utf-8 -*-
#! uer/bin/python
import xlwt
from bs4 import BeautifulSoup
import requests
import re
import time

def ask_url(url):
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49'
    }

    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    Cookie = 'yfx_c_g_u_id_10001341=_ck21043016293314681157932513071; yfx_mr_f_10001341=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_10001341=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10001341=; yfx_f_l_v_t_10001341=f_t_1619771373457__r_t_1619771373457__v_t_1619776818808__r_c_0'

    param={
        'Accept':Accept,
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':Cookie,
        'Host':'www.pgm.org.cn',
        'Referer':'http://www.pgm.org.cn/pgm/zixun/zixun.shtml',
        'Upgrade-Insecure-Requests':'1',
    }
    response = requests.get(url=url,params=param,headers=header)
    response.encoding = 'utf-8'
    data = response.text
    return data

if __name__ == '__main__':
    url = 'http://www.pgm.org.cn/pgm/wfdt/list.shtml'
    data = ask_url(url)
    Get_All_Url = re.findall('<a href="../../pgm/wfdt/(.*?)"',data)
    counter = 1
    for i in  Get_All_Url:
        URL = 'http://www.pgm.org.cn/pgm/wfdt/' + i
        respone = ask_url(URL)
        # title = re.findall('class="title">(.*?)<',respone)
        with open('News/恭王府第' + str(counter) + '条新闻.html','w',encoding='utf-8') as file:
            file.write(respone)
        counter += 1
    
    # print(data)
    # with open('News/恭王府的新闻.html','w',encoding='utf-8') as file:
    #     file.write(data)
    # soup = BeautifulSoup(open('News/恭王府的新闻.html',encoding='utf-8'),'html.parser')
    # find = soup.find_all('span',class_='time fr')
    # for i in  find:
    #     print(i.string)



# t_list=bs.find_all('p',style="text-indent:2em;")
# t_list=str(t_list)

# 去除指定标签页
# [s.extract() for s in bs('p',style="text-align:center;")]

# method = '[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]||[0-9]'
# txt=re.findall(method,t_list)
