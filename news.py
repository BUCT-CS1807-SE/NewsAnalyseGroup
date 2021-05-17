#
# author:   李明宇
#
# update:
#       时间    姓名   行为
#    2021-5-10 赵云启 适配服务器
#    2021-5-13 赵云启 分类模块
#    2021-5-13 赵云启 分类模块升级
import datetime
import re

import pymysql
import requests
import xlrd
import xlwt
from bs4 import BeautifulSoup

from classifier2 import get_label1, get_label2

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49',
}
__URL = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86%E6%96%B0%E9%97%BB&medium=0'

config = {
    # 'deadline': {'days':-1},
    'reseach': '博物馆新闻',
    'excel_title': ['ID',  # 不写为空
                    '标题',
                    '作者',
                    '新闻发布时间',
                    '新闻内容',
                    '原文链接',
                    '爬取时间',
                    '相关博物馆',  # 不写为空
                    '分类1',  # 不写为空
                    '分类2',  # 不写为空
                    '分类3'  # 不写为空
                    ]
}


def insert(cur, sql, args):
    cur.execute(sql, args)


def get_stop_time():
    return datetime.datetime.now() + datetime.timedelta(days=-1)


def init_excel():
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=False)
    worksheet = workbook.add_sheet('Sheet1')
    for i in range(len(config['excel_title'])):
        worksheet.write(0, i, config['excel_title'][i])

    return workbook, worksheet


def time_conversion(str_time):
    # print("ok")
    # print(str_time)
    time__ = '2021-' + str_time[0].split()[0]
    time_str = time__.split('-')
    newstime = datetime.datetime(int(time_str[0]), int(time_str[1]), int(time_str[2]))
    return newstime


def to_mysql_database(xlsfile, YMD):
    global cur, conn
    try:
        # 服务器
        # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', db='rouyi-vue', charset='utf8')
        # 本地
        conn = pymysql.connect(host='localhost', port=8889, user='root', passwd='123123', db='test', charset='utf8')
    except Exception as e:
        return e.args
    else:
        cur = conn.cursor()

        sql = "insert into news(Title,Author,Time,Content,Link,GetTime,ClassificationOne,ClassificationTwo) values (%s,%s,%s,%s,%s,%s,%s,%s)"

        params = []
        readbook = xlrd.open_workbook(xlsfile)
        sheet = readbook.sheet_by_index(0)
        nrows = sheet.nrows
        # ncols = sheet.ncols
        for i in range(1, nrows):
            t = (sheet.cell(i, 1).value,
                 sheet.cell(i, 2).value,
                 sheet.cell(i, 3).value,
                 sheet.cell(i, 4).value,
                 sheet.cell(i, 5).value,
                 sheet.cell(i, 6).value,
                 sheet.cell(i, 8).value,
                 sheet.cell(i, 9).value,
                 )
            params.append(t)

        print("params:",params)

        cur.executemany(sql, params)
        conn.commit()
        print("插入成功")
    finally:
        # pass
        cur.close()
        conn.close()

    pass


def to_excel(worksheet, counter, msg):
    worksheet.write(counter, 1, msg[0])
    worksheet.write(counter, 2, msg[1])
    worksheet.write(counter, 3, msg[2])
    worksheet.write(counter, 4, msg[3])
    worksheet.write(counter, 5, msg[4])
    worksheet.write(counter, 6, msg[5])
    worksheet.write(counter, 8, msg[6])
    worksheet.write(counter, 9, msg[7])


def main():
    BREAK = False
    STOPTIME = get_stop_time()
    # STOPTIME = datetime.datetime(2021,5,11,0,0,0,0)
    # nowtime = datetime.datetime(2021,5,12,0,0,0,0)
    nowtime = datetime.datetime.now()
    timeYMD = str(nowtime.year) + '-' + str(nowtime.month) + '-' + str(nowtime.day)
    print(timeYMD)
    print("爬虫程序启动,正在爬取在晚于",STOPTIME,"发布的新闻")
    # 运行程序
    workbook, worksheet = init_excel()
    counter = 1
    response = requests.get(__URL, headers=header)
    data = response.text
    # print(data)
    html_url = re.findall('<h3 class="news-title_1YtI1"><a href="https://baijiahao.baidu.com/(.*?)" target=',
                          data, re.S)
    print(html_url)
    for i in html_url:
        URL = 'https://baijiahao.baidu.com/' + i
        try:
            res = requests.get(URL, headers=header)
            data0 = res.text
            time = re.findall('<span>发布时间:(.*?)</span>', data0, re.S)
            print(time)
            if time_conversion(time) < STOPTIME:
                print(time,STOPTIME)
                print(time_conversion(time), ' -- stop')
                break
            title = re.findall('<h2 class="index-module_articleTitle_28fPT">(.*?)</h2>', data0, re.S)
            class1 = get_label1(title[0])
            class2 = get_label2(title[0])
            # class2 = ''
            print(class1, class2)
            # <h2 class="index-module_articleTitle_28fPT">坐标重庆沙坪坝！巴蜀古代建筑博物馆开馆了，先来一睹为快</h2>
            # <span>发布时间: 19-11-06</span>
            from0 = re.findall('<span class="index-module_accountAuthentication_3BwIx">(.*?)</span>', data0,
                               re.S)
            # <span class="index-module_accountAuthentication_3BwIx">重庆晚报慢新闻官方帐号</span>
            bs = BeautifulSoup(res.text, 'html.parser')
            txt = bs.find_all('p')
            content = ""
            for j in txt:
                if j.string:
                    content = content + j.string
            msg = [title,
                   from0,
                   timeYMD,
                   content,
                   URL,
                   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   class1,
                   class2]
            to_excel(worksheet, counter, msg)
            counter += 1
        except:
            continue
    for k in range(1, 10):
        # https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86%E6%96%B0%E9%97%BB&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn=10
        url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86%E6%96%B0%E9%97%BB&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn=' + str(
            k) + '0'
        response = requests.get(url, headers=header)
        data = response.text
        html_url = re.findall(
            '<h3 class="news-title_1YtI1"><a href="https://baijiahao.baidu.com/(.*?)" target=', data, re.S)
        # print(html_url)
        for i in html_url:
            URL = 'https://baijiahao.baidu.com/' + i
            try:
                res = requests.get(URL, headers=header)
                data0 = res.text
                time = re.findall('<span>发布时间:(.*?)</span>', data0, re.S)
                print(time)
                if time_conversion(time) < STOPTIME:
                    print(time_conversion(time), ' -- stop')
                    BREAK = True
                    break
                title = re.findall('<h2 class="index-module_articleTitle_28fPT">(.*?)</h2>', data0, re.S)
                class1 = get_label1(title[0])
                class2 = get_label2(title[0])
                print(class1, class2)
                # <h2 class="index-module_articleTitle_28fPT">坐标重庆沙坪坝！巴蜀古代建筑博物馆开馆了，先来一睹为快</h2>
                # <span>发布时间: 19-11-06</span>
                from0 = re.findall('<span class="index-module_accountAuthentication_3BwIx">(.*?)</span>', data0,
                                   re.S)
                # <span class="index-module_accountAuthentication_3BwIx">重庆晚报慢新闻官方帐号</span>
                bs = BeautifulSoup(res.text, 'html.parser')
                txt = bs.find_all('p')
                content = ""
                for j in txt:
                    if j.string:
                        content = content + j.string
                # print(s)
                # today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                msg = [title,
                       from0,
                       timeYMD,
                       content,
                       URL,
                       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       class1,
                       class2]
                to_excel(worksheet, counter, msg)
                counter += 1
            except:
                continue

        if BREAK:
            break
    workbook.save('baidu' + timeYMD + '.csv')
    # to_mysql_database('baidu' + timeYMD + '.csv', timeYMD)


if __name__ == '__main__':
    main()
