# 
# author:   赵云启
#
# update:
#       时间    姓名   行为
#    2021-5-16 赵云启 适配服务器
#    2021-5-16 赵云启 分类模块

# 管理员联系方式：赵云启
#        电话 18512181356，微信 z18512181356


import datetime

import pymysql
import xlrd
import xlwt
from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from classifier1 import *

# 设置chrome为无界面浏览器
options = Options()
options.add_argument('-headless')

config__ = {
    'get_label': True
    'to_mysql': True
}

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


# 只爬取网易新闻
def analyse_index(name):  # 输入博物馆名称
    print(name)
    all_sources = []
    links = []
    browser = webdriver.Firefox(options=options)
    url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=' + name + '&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8'
    browser.get(url)
    page_text = browser.page_source
    tree = etree.HTML(page_text)
    news_sources = tree.xpath(
        '//div[@class="news-source"]/span[@class="c-color-gray c-font-normal c-gap-right"]/text()')
    all_sources = all_sources + news_sources
    tree = etree.HTML(page_text)
    link = tree.xpath('//h3[@class="news-title_1YtI1"]/a/@href')
    # item=tree.xpath('//h3[@class="news-title_1YtI1"]/a/text()')
    links = links + link
    for i in range(10, 100, 10):
        url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=故宫博物院&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=' + str(
            i)
        browser.get(url)
        page_text = browser.page_source
        tree = etree.HTML(page_text)
        news_sources = tree.xpath(
            '//div[@class="news-source"]/span[@class="c-color-gray c-font-normal c-gap-right"]/text()')
        all_sources = all_sources + news_sources
        tree = etree.HTML(page_text)
        link = tree.xpath('//h3[@class="news-title_1YtI1"]/a/@href')
        links = links + link
    return all_sources, links


def screen(all_sources, links):  # 将人民资讯和新闻网的新闻提取出来
    new_all_sources = []
    new_all_links = []
    for i in range(len(all_sources)):
        if all_sources[i] == '人民资讯' or all_sources[i] == '网易新闻':
            new_all_sources.append(all_sources[i])
            new_all_links.append(links[i])
    return new_all_sources, new_all_links


# 进行爬取
def scrapy(all_new_sources, links):  # 访问浏览器中的内容
    dates = []
    contents = []
    themes = []
    browser = webdriver.Firefox(options=options)
    for i in range(len(all_new_sources)):
        if all_new_sources[i] == '人民资讯':  # 人民资讯网分析
            browser.get(links[i])
            page_text = browser.page_source
            tree = etree.HTML(page_text)
            date = tree.xpath('//div[@class="index-module_articleSource_2dw16"]/span/text()')
            content = tree.xpath('//span[@class="bjh-p"]/text()')
            # +++++后加++++
            item = tree.xpath('//h2[@class="index-module_articleTitle_28fPT"]/text()')
            themes.append(item)
            # ------------
            date = '2021-' + date[0].split(':')[1]
            date = date.replace(' ', '')
            dates.append(date)  # 将发布时间修正之后在放到其中
            string = ''
            for i in range(len(content)):
                string = string + content[i]
            contents.append(string)
        else:  # 网易新闻网分析
            browser.get(links[i])
            page_text = browser.page_source
            tree = etree.HTML(page_text)
            date = tree.xpath('//div[@class="post_info"]/text()')
            content = tree.xpath('//div[@class="post_body"]/p/text()')
            # 后————————加
            item = tree.xpath('//h1[@class="post_title"]/text()')
            themes.append(item)
            # ———————————
            date = date[0].split(' ')
            for i in range(len(date)):
                if '-' in date[i]:
                    dates.append(date[i])
                    break
            string = ''
            for i in range(len(content)):
                string = string + content[i]
            contents.append(string)
    return dates, contents, themes


def screen_date(start, end, dates, content, all_new_sources, links, themes):  # 输入起始时间和终止时间，要求的格式为2021-1-1
    new_content = []
    new_dates = []
    # ————————新加————————
    new_sources = []
    new_links = []
    new_themes = []
    # ———————————————————
    flag = 1
    start = start.split('-')
    end = end.split('-')
    start_number = int(start[0]) * 365 + int(start[1]) * 30 + int(start[2])
    end_number = int(end[0]) * 365 + int(end[1]) * 30 + int(end[2])
    for i in range(len(dates)):
        date = dates[i].split('-')
        number = int(date[0]) * 365 + int(date[1]) * 30 + int(date[2])
        if number < start_number or number > end_number:
            continue
        new_content.append(content[i])
        new_dates.append(dates[i])
        # ————————新加————————
        new_sources.append(all_new_sources[i])
        new_links.append(links[i])
        new_themes.append(themes[i])
        # ———————————————————
    print("new_dates", new_dates)
    print("new_content", new_content)
    # ———————————————————
    print("new_links", new_links)
    print("new_sources", new_sources)
    print("new_themes", new_themes)
    # ———————————————————
    return new_themes, new_sources, new_dates, new_content, new_links


def init_excel():
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=False)
    worksheet = workbook.add_sheet('Sheet1')
    for i in range(len(config['excel_title'])):
        worksheet.write(0, i, config['excel_title'][i])

    return workbook, worksheet


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def to_excel(worksheet, counter, msg):
    worksheet.write(counter, 1, msg[0])
    worksheet.write(counter, 2, msg[1])
    worksheet.write(counter, 3, msg[2])
    worksheet.write(counter, 4, msg[3])
    worksheet.write(counter, 5, msg[4])
    worksheet.write(counter, 6, msg[5])
    worksheet.write(counter, 7, msg[6])
    worksheet.write(counter, 8, msg[7])
    worksheet.write(counter, 9, msg[8])


def to_mysql_database(xlsfile, YMD):
    global cur, conn
    try:
        # 服务器
        # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', db='rouyi-vue',
        #                        charset='utf8')
        # 本地
        conn = pymysql.connect(host='localhost', port=8889, user='root', passwd='123123', db='test', charset='utf8')
    except Exception as e:
        return e.args
    else:
        cur = conn.cursor()

        sql = "insert into news(Title,Author,Time,Content,Link,GetTime,MumName,ClassificationOne,ClassificationTwo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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
                 sheet.cell(i, 7).value,
                 sheet.cell(i, 8).value,
                 sheet.cell(i, 9).value,
                 )
            params.append(t)

        print(params)

        cur.executemany(sql, params)
        conn.commit()
        print("插入成功")
    finally:
        # pass
        cur.close()
        conn.close()

    pass


if __name__ == '__main__':
    # name = input("请输入博物馆名称：")
    # start = input("请输入新闻的起始时间：")
    # end = input("请输入新闻的终止时间：")

    nowtime = datetime.datetime.now()
    timeYMD = str(nowtime.year) + '-' + str(nowtime.month) + '-' + str(nowtime.day)

    workbook, worksheet = init_excel()
    name = "故宫博物院"
    start = "2021-1-1"
    end = "2021-5-10"

    all_sources, links = analyse_index(name)
    print("ok")
    all_new_sources, links = screen(all_sources, links)
    print("ook")
    dates, contents, themes = scrapy(all_new_sources, links)
    print("oook")
    new_themes, new_sources, new_dates, new_content, new_links = screen_date(start, end, dates, contents,
                                                                             all_new_sources, links, themes)
    for i in range(len(new_themes)):
        msg = [new_themes[i][0],
               new_sources[i],
               new_dates[i],
               new_content[i],
               new_links[i],  # str
               now(),
               name,
               ]
        if config__['get_label']:
            msg.append(get_label1(msg[0]))
            msg.append(get_label2(msg[0]))
        else:
            msg.append('')
            msg.append('')
        to_excel(worksheet, i+1, msg)
    workbook.save(name+timeYMD+'.csv')
    if config__['to_mysql']:
        to_mysql_database(name+timeYMD+'.csv',timeYMD)
