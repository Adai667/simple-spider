#-*- coding= utf-8 -*-
import sys
import re
import urllib.request
import xlwt
from bs4 import BeautifulSoup
import random
import time 

def main():
    baseurl = "https://www.chegg.com/homework-help/questions-and-answers/"
    dst = ".\\chegg.xls"
    datalist = []
    for i in range(0, 4):
        baseurl = baseurl + subjects[i] + 'archive-2021-february-'
        data = getData(baseurl)
        datalist.append(data)
    saveData(datalist, dst)

findnum = re.compile(r'"totalQuestions":[0-9]*,"')
subjects = ["statistics-and-probability-", "calculus-", "algebra-", "economics"]
my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
]
ips = ['160.16.203.39:80', '103.134.168.239:80', '3.225.148.200:80', '3.224.205.253:80', '143.198.192.212:80', '182.46.229.158:9999']

def askURL(url):
    random_header=random.choice(my_headers)
    random_ip = random.choice(ips)
    proxies = {'http': random_ip, 'https': random_ip}
    urlhandle = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(urlhandle)
    urllib.request.install_opener(opener)
    head = {"User-Agent": random_header, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US, en; q=0.8", "Path": "/scripttemplates/6.10.0/assets/otPcCenter.json",
    "Origin": "https://www.chegg.com"}
    req = urllib.request.Request(url, headers = head)
    html = ""
    while True:
        try:
            response = urllib.request.urlopen(req)
            html = response.read()
            html = str(html)
            if (html == '403' or html == '404'):
                print("found")
                html = askURL(url)
            break
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
    return html


def getData(baseurl):
    data = []
    for i in range(1, 28):
        if (i < 10):
            url = baseurl + '0' + str(i)
        else:
            url = baseurl + str(i)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('script'): 
            if item:
                item = str(item)
                numbers = re.findall(findnum, item)
                for num in numbers:
                    print(num)
                    data.append(num)
            else:
                print("something wrong happened")  
        time.sleep(1)  
    return data

def saveData(datalist, dst):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
    for i in range(0, 4):
        length = len(datalist[i])
        for j in range(0, length):
            tmp = datalist[j][15:-1]
            print(tmp)
            sheet.write(j + 1, i + 1, tmp)
    book.save(dst)
    print("success!")


if __name__ == "__main__":
    main()
