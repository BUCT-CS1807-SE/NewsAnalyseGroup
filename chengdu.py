import xlwt
from bs4 import BeautifulSoup
import requests
import re
import time
import execjs  # 执行js代码

header = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49',
}





if __name__ == '__main__':
    counter=1
    workbook = xlwt.Workbook(encoding = 'utf-8',style_compression=False)
    worksheet = workbook.add_sheet('Sheet1')
    excel_title = ['新闻标题','新闻内容','新闻时间','原文链接','爬取时间']
    for i in range(0,5):
        worksheet.write(0,i,excel_title[i])
    for k in range(1,186):
        url = 'https://www.cdmuseum.com/xinwen/index_'+str(k)+'.html'
        response = requests.get(url,headers=header)
        data = response.text
        html_url = re.findall('<a href="/xinwen/20(.*?)">',data,re.S)
        print(html_url)
        for i in html_url:
            URL='https://www.cdmuseum.com/xinwen/20'+i
            #print(URL)
            
            res = requests.get(URL,headers = header)
            data0 = res.text
            time = re.findall('<span>(.*?)</span>',data0,re.S)
            title = re.findall('<p class="tt2 tt02">(.*?)</p>',data0,re.S)
                #txt = re.findall('2em; ">(.*?)</p>',data0,re.S)
                #<p style="text-indent: 2em; text-align: center;">你能找到我们吗</p>
            bs=BeautifulSoup(res.text,'html.parser')
            txt = bs.find_all('p')
            #print(time[1] + title)
           # worksheet.write("infoPlist",cell_overwrite_ok=True)
            s=""
            for j in txt:
                if j.string:
                    s=s+j.string
            #print(s)
            worksheet.write(counter,0,title)
            worksheet.write(counter,1,s)
            worksheet.write(counter,2,time[1])
            worksheet.write(counter,3,URL)
            worksheet.write(counter,4,"2021-05-06")
            counter+=1
            print(counter)
        #print(counter)
    workbook.save('成都博物馆.xls')



    

