#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests
import os
from multiprocessing import Pool


def get_page(offset):
    fl_url = "https://818ps.com/search/0-0-0-0-0-null-31_1_0-0-0/" + str(offset) + ".html?route_id=15634482253883&route=1,3,&after_route=1,3"
    data = requests.get(fl_url).text
    tj = "/detail/(.*?).html"
    p = re.compile(tj).findall(data)
    p = list(set(p))
    return p


def save_page(p):
    try:
        for i in p:
            # free = str(i)
            new_url = "https://818ps.com/detail/" + str(i) + ".html"
            new_data = requests.get(new_url).text
            new_tj = '//img.tuguaishou.com/ips_templ_preview/(.*?)"\salt.*title="(.*?)"/>'
            q = re.compile(new_tj).findall(new_data)
            for j, p in q:
                tup_url = "https://img.tuguaishou.com/ips_templ_preview/" + str(j)
                # file = "./bing/a/" + str(a) +str(i) + str(j) + ".jpg"
                p = re.sub('/', '_',str(p))
                print("正在下载编号:" + p)
                img_path = 'img'
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                imagetemp = requests.get(tup_url).content
                file_path =  img_path + os.path.sep + p + ".jpg"
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(imagetemp)
                    print("下载完成")
                else:
                        print('已经下载', file_path)
    except requests.exceptions.InvalidURL as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def main(offset):
    p = get_page(offset)
    save_page(p)


group_start = 1  #起始页数
group_end = 10   #结束页数
if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 1 for x in range(group_start, group_end+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()