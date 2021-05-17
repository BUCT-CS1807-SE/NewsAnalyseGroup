import time
import xlwt
from selenium import webdriver
import datetime

start = 1
value = {
    'id': start,
    'title': '',
    'now_time': '',
    'content': '',
    'url': "",
    'museum': '南京博物馆'

}
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('My Worksheet')
worksheet.write(0,0, label = 'id')
worksheet.write(0,1, label = '标题')
worksheet.write(0,2, label = '作者')
worksheet.write(0,3, label = '新闻发布时间')
worksheet.write(0,4, label = '新闻内容')
worksheet.write(0,5, label = '原文链接')
worksheet.write(0,6, label = '爬取时间')
worksheet.write(0,7, label = '相关博物馆')

counter=1
driver = webdriver.Chrome()
id_start = 356054
id_end = 337178
for page in range(337178, 356054):
    link="http://www.njmuseum.com/zh/newsDetails?id=" +str(page)
    driver.get("http://www.njmuseum.com/zh/newsDetails?id=" +str(page))
    time.sleep(2)
    now_time = datetime.datetime.now()
    nntime=datetime.datetime.now().strftime('%Y-%m-%d')
    title = driver.find_element_by_xpath("//h2[@class='article-title ']/span")
    new_time=driver.find_element_by_tag_name("em")
    content=driver.find_element_by_class_name("content")
    print("正在爬取："+"http://www.njmuseum.com/zh/newsDetails?id=" + str(page))
    worksheet.write(counter, 0, label=str(counter))
    worksheet.write(counter, 1, label=title.text)
    worksheet.write(counter, 3, label=new_time.text)
    worksheet.write(counter, 4, label=content.text)
    worksheet.write(counter, 5, label=link)
    worksheet.write(counter, 6, label=nntime)
    worksheet.write(counter, 7, label="南京博物馆")

    workbook.save('Excel_Museum.xls')
    counter=counter+1


    # print(title.text)
   # print(new_time.text)
   # print(content.text)
