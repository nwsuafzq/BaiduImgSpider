#coding:utf-8
import requests
import re
import os
import urllib2
url = r'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%95%8A%E5%93%88'
#query_words = '人打哈欠'.decode('utf8').encode('gbk') 
#query_item = urllib.quote(query_words)
dirpath = r'F:\img'
#url1=url + query_item

html = requests.get(url).text
urls = re.findall(r'"objURL":"(.*?)"', html)

if not os.path.isdir(dirpath):
    os.mkdir(dirpath)

index = 1
for url in urls:
    print("Downloading:", url)
    try:
        res = requests.get(url)
        if str(res.status_code)[0] == "4":
            print("未下载成功：", url)
            continue
    except Exception as e:
        print("未下载成功：", url)
    filename = os.path.join(dirpath, str(index) + ".jpg")
    with open(filename, 'wb') as f:
        f.write(res.content)
        index += 1

print("下载结束，一共 %s 张图片" % index)