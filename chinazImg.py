# -*- coding:utf-8 -*-
# from mysql.MysqlHelp import MysqlHelp
import re
import requests
import time
from lxml import etree
from selenium import webdriver
from urllib import error
from bs4 import BeautifulSoup
import os

BASE_URL = "https://sc.chinaz.com"  #  网站地址
BASE_PATH = "/tupian/dongman.html"  #  网站地址
# 模拟浏览器 请求数据 伪装成浏览器向网页提取服务
header = {
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Upgrade-Insecure-Requests': '1'
}
MAXIMAL_RETRY = 3 # 默认重试次数


#  定义一个类，用于专门爬取页面，得到想要的内容
class Procuder(object):
    src_and_name = []  #  定义一个列表来放视频的标题和播放地址
    soup = ''
    link_ls = {}

    # 定义一个爬取并解析页面的函数
    def get_soup(self, url):
        response = requests.get(url, headers = header)
        # 修改字符集（可选）
        new_charset = 'utf-8'  # 替换为你希望使用的字符集
        response.encoding = new_charset
        # 解析网页内容
        html_content = response.text
        self.soup = BeautifulSoup(html_content, 'html.parser')


    # 获取页面分页信息
    def get_page(self):
        # 获取分页
        alinkLs = self.soup.find('div', class_='new-two-page-box').find_all('a')

        # 遍历 link
        for alink in alinkLs:
            if alink.text.isnumeric():
                self.link_ls['num'] = alink.text;
                self.link_ls['link'] = alink.get('href');


    # 获取每个分页内图片url和文本
    def get_page_img(self):
        num = int(self.link_ls['num'])
        link = self.link_ls['link']
        link_arr = link.split("_")
        page_link = link_arr[0] + '_num.html'

        # 图片列表循环
        for i in range(num):
            page = ''
            if page != 1:
                page = '_' + str(i + 1)

            page_num_link = page_link.replace("_num", page, 1)
            print(page_num_link)

        # main_div = soup.find('div', class_='com-img-txt-list')
        # son_div = main_div.find_all('div', class_="item")

        # print(son_div)

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
        # 获取页面内容
        self.get_soup(url)
        # 获取页面分页
        self.get_page()
        # 获取分页图片
        self.get_page_img()


def main():
    t = Procuder()
    t.run()

if __name__ == '__main__':
    main()
