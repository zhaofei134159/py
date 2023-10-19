# -*- coding:utf-8 -*-
from mysql.MysqlHelp import MysqlHelp
import re
import requests
import time
from lxml import etree
from selenium import webdriver
import os

BASE_URL = "https://sc.chinaz.com"  #  网站地址
BASE_PATH = "/tupian/dongman.html"  #  网站地址
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
MAXIMAL_RETRY = 3 # 默认重试次数


#  定义一个类，用于专门爬取页面，得到想要的内容
class Procuder(object):
    src_and_name = []  #  定义一个列表来放视频的标题和播放地址

    #  定义一个爬取并解析页面的函数，得到要下载视频的url和视频名字
    def get_data(self, url):
        try:
            #  请求首页，得到BASE_URL中槽的数字
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            text = response.text
            html = etree.HTML(text)
        except:
            print('爬取首页时出现错误!')

        print(html)


    def InsertDB(self,data):
        # 连接 mysql，获取连接的对象
        sql = "INSERT into zf_video(`name`,`path`,`episodes`) values(%s,%s,%s)"
        db = MysqlHelp()
        db.insert_delete_update(sql,data)

    # 重试
    def retry_url(self,url,times=0):
        time.sleep(1)
        try:
            return requests.get(url)
        except Exception as e:
            if times >= MAXIMAL_RETRY:
                print('超过重试次数')
                raise(e) # will stop the program without further handling
            else:
                times += 1
                print('重试第'+times+'次')
                return run_with_retry(url,times)

    def run(self):
        url = BASE_URL + BASE_PATH
        self.get_data(url)


def main():
    t = Procuder()
    t.run()

if __name__ == '__main__':
    main()
