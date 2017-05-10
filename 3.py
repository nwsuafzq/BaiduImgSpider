#coding:utf-8
import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# ���ó�ʱ
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # ˯��ʱ��
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0

    # ��ȡͼƬurl���ݵ�
    # t ����ͼƬʱ����
    def __init__(self, t=0.1):
        self.time_sleep = t

    # ��ʼ��ȡ
    def __getImages(self, word='��Ů'):
        search = urllib.parse.quote(word)
        # pn int ͼƬ��
        pn = self.__start_amount
        while pn < self.__amount:

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # ����header��ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=headers)
                page = urllib.request.urlopen(req)
                data = page.read().decode('utf8')
            except UnicodeDecodeError as e:
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print("-----socket timout:", url)
            else:
                # ����json
                json_data = json.loads(data)
                self.__saveImage(json_data, word)
                # ��ȡ��һҳ
                print("������һҳ")
                pn += 60
            finally:
                page.close()
        print("�����������")
        return

    # ����ͼƬ
    def __saveImage(self, json, word):

        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # �ж������Ƿ��ظ�����ȡͼƬ����
        self.__counter = len(os.listdir('./' + word)) + 1
        for info in json['imgs']:
            try:
                if self.__downloadImage(info, word) == False:
                    self.__counter -= 1
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                pass
            except Exception as err:
                time.sleep(1)
                print(err);
                print("����δ֪���󣬷�������")
                continue
            finally:
                print("С��ͼ+1,����" + str(self.__counter) + "��С��ͼ")
                self.__counter += 1
        return

    # ����ͼƬ
    def __downloadImage(self, info, word):
        time.sleep(self.time_sleep)
        fix = self.__getFix(info['objURL'])
        urllib.request.urlretrieve(info['objURL'], './' + word + '/' + str(self.__counter) + str(fix))

    # ��ȡ��׺��
    def __getFix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # ��ȡǰ׺
    def __getPrefix(self, name):
        return name[:name.find('.')]

    # page_number ��Ҫץȡ����ҳ�� ��ץȡͼƬ����Ϊ ҳ��x60
    # start_page ��ʼҳ��
    def start(self, word, spider_page_num=1, start_page=1):
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__getImages(word)


crawler = Crawler(0.05)
# crawler.start('��Ů', 1, 2)
crawler.start('����Ԫ �Ը�', 3, 3)
# crawler.start('˧��', 5)