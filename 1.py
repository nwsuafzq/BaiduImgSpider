#!/usr/bin/python
#-*- coding: UTF-8 -*-

# creat  by  lilin  

import os
import re
import sys
import json
import urllib

# http://pic.sogou.com/pics?query=%C6%FB%B3%B5&mode=1&start=144&reqType=ajax&reqFrom=result&tn=0

#http://pic.sogou.com/pics?query=%B4%F2%B9%FE%C7%B7&w=05002100&p=40030500&_asf=pic.sogou.com&_ast=1493904488&sc=index&oq=dahaqian&ri=0&sourceid=sugg&sut=7487&sst0=1493904487711
baseurl = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%95%8A%E5%93%88'
#baseurl = 'https://image.baidu.com/pics?query='
#j_1 = '&mode=1&start='
#j_2 = '&reqType=ajax&reqFrom=result&tn=0'
start = 0       # start index
end = 48 * 20   # total count , about 20 pages pic
save_path = 'sg_pic_down/'
if os.name == 'nt':
    save_path = 'sg_pic_down\\'
if not os.path.exists(save_path):
    os.makedirs(save_path)
pic_index = 0
print 'cur encoding:' + sys.stdin.encoding
query_words = '人打哈欠'.decode('utf8').encode('gbk')   #decode解码encode编码
query_item = urllib.quote(query_words) #将url数据获取之后，将其编码，从而适用于url字符串中，使其能被打印和web服务器接收
print 'find[%s][%s]'%(query_words,query_item)

def format_url(query_str,start):
    return baseurl + query_str

pic_url_start = '"pic_url":"'
pic_url_start_len = len(pic_url_start)
def find_one_pic(page,start):
    m = page.find(pic_url_start,start)  #字符串中查找子字符串，如果找到返回首字母位置，如果找不到返回-1
    if m >= 0:
        n = page.find('"',m+pic_url_start_len)
        if n >= 0:
            s = page[m+pic_url_start_len:n]
            urls = s.split('/')
            if len(urls) > 0:
                return (s,n,urls[-1])
    return None
def split_picurl(page):
    ret = []
    start = 0
    while True:
        info = find_one_pic(page,start)
        if info:
            start = info[1]
            ret.append((info[0],info[2]))
        else:
            break
    return ret
def sg_pic_down(index):
    global pic_index  #全局变量
    u = format_url(query_item,index)
    #print 'get pic list from[%s]'%(u)
    try:
        f = urllib.urlopen(u)
        page = f.read()   #读取该页
        pics = split_picurl(page)
        for item in pics:
            local_f = save_path + item[1]
            #with open(local_f,'wb') as lf:
            #    pic_f = urllib.urlopen(item[0])
            #    lf.write(pic_f.read())
            #print 'pic[%s][%s]'%(s,urls[-1])
            try:
                urllib.urlretrieve(item[0],local_f)
                print 'down[%s]->[%s]'%(item[0],local_f)
            except Exception as ex:
                print 'Exception.urlretrieve:'+str(ex)
        return len(pics)
    except UnicodeDecodeError as ude:
        print "UnicodeDecodeError:"+str(ude)
    except Exception as ex:
        print 'Exception:'+str(ex)

if __name__ == '__main__':
    index = start
    while True:
        if index >= end:
            break
        try:
            index += sg_pic_down(index)
        except KeyboardInterrupt as ki:
            print 'KeyboardInterrupt Close'
            break






    
