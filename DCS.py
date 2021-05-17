import pandas as pd
import numpy as np
import openpyxl
import requests
from selenium import webdriver
from lxml import etree
from selenium.webdriver.firefox.options import Options

# 设置chrome为无界面浏览器
options = Options()
options.add_argument('-headless')


# 只爬取网易新闻
def analyse_index(name):  # 输入博物馆名称
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
    browser = webdriver.Firefox(options=options)
    for i in range(len(all_new_sources)):
        if all_new_sources[i] == '人民资讯':  # 人民资讯网分析
            browser.get(links[i])
            page_text = browser.page_source
            tree = etree.HTML(page_text)
            date = tree.xpath('//div[@class="index-module_articleSource_2dw16"]/span/text()')
            content = tree.xpath('//span[@class="bjh-p"]/text()')
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
            date = date[0].split(' ')
            for i in range(len(date)):
                if '-' in date[i]:
                    dates.append(date[i])
                    break
            string = ''
            for i in range(len(content)):
                string = string + content[i]
            contents.append(string)
    return dates, contents


def screen_date(start, end, dates, content):  # 输入起始时间和终止时间，要求的格式为2021-1-1
    new_content = []
    new_dates = []
    flag = 1
    start = start.split('-')
    end = end.split('-')
    start_number=int(start[0])*365+int(start[1])*30+int(start[2])
    end_number=int(end[0])*365+int(end[1])*30+int(end[2])
    for i in range(len(dates)):
        date = dates[i].split('-')
        number=int(date[0])*365+int(date[1])*30+int(date[2])
        if number<start_number or number>end_number:
            continue
        new_content.append(content[i])
        new_dates.append(dates[i])
    print(new_dates)
    print(new_content)


# name=input("请输入博物馆名称：")
# start=input("请输入新闻的起始时间：")
# end=input("请输入新闻的终止时间：")
name = "故宫博物院"
start = "2021-1-1"
end = "2021-5-10"

all_sources, links = analyse_index(name)
all_new_sources, links = screen(all_sources, links)
dates, contents = scrapy(all_new_sources, links)
screen_date(start, end, dates, contents)