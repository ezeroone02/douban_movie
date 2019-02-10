# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import random
import requests
import configparser
import constants
import json
from login import CookiesHelper
from page_parser import MovieParser
from utils import Utils
from utils import ForbiddenError
from storage import DbHelper
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')

# 获取模拟登录后的cookies
cookie_helper = CookiesHelper.CookiesHelper(
    config['douban']['user'],
    config['douban']['password']
)
cookies = cookie_helper.get_cookies()
print(cookies)


# 实例化爬虫类和数据库连接工具类
movie_parser = MovieParser.MovieParser()
db_helper = DbHelper.DbHelper()

Utils.Utils.mkdir(constants.RATIO_POSTER_PATH)
Utils.Utils.mkdir(constants.DATA_PATH)

search_subject_url_prefix = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s"
start_value = 0
while True:

    log_name = constants.DATA_PATH + "\\start_value.txt"
    log_file = open(log_name, 'w')
    log_file.write(str(start_value))
    log_file.close()

    search_subject_url = search_subject_url_prefix % start_value
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    try:
        # 获取豆瓣页面(API)数据
        r = requests.get(
            search_subject_url,
            headers=headers,
            cookies=cookies,
            # proxies=constants.proxies
        )
        if r.status_code == '403':
            print(search_subject_url+"403")
            logging.error(search_subject_url+"403")
            raise ForbiddenError
            break
        r.encoding = 'utf-8'
        search_subject_result = json.loads(r.text)
        id_list = []
        if not search_subject_result["data"]:
            print(search_subject_url+"返回的数据为" + search_subject_result)
            logging.error(search_subject_url+"返回的数据为" + search_subject_result)
            break

        for subject in search_subject_result["data"]:
            print(subject["title"]+subject["url"])
            logging.info(subject["title"]+subject["url"])
            id_list.append(subject["id"])

        Utils.Utils.request_and_parse_movies(id_list, movie_parser, db_helper, cookies)
    except ForbiddenError:
        print("403forbidden")
        break

    print("start value %s done" % start_value)
    start_value += 20

    Utils.Utils.delay(1, 2)

    if start_value > 200000:
        break

# # 读取抓取配置
# START_ID = int(config['common']['start_id'])
# END_ID = int(config['common']['end_id'])
#
# # 通过ID进行遍历
# for i in range(START_ID, END_ID):
#
#     headers = {'User-Agent': random.choice(constants.USER_AGENT)}
#
#     # 获取豆瓣页面(API)数据
#     r = requests.get(
#         constants.URL_PREFIX + str(i),
#         headers=headers,
#         cookies=cookies
#     )
#     r.encoding = 'utf-8'
#
#     # 提示当前到达的id(log)
#     print('id: ' + str(i))
#
#     # 提取豆瓣数据
#     movie_parser.set_html_doc(r.text)
#     movie = movie_parser.extract_movie_info()
#
#     # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
#     if not movie:
#         Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
#         continue
#
#     # 豆瓣数据有效，写入数据库
#     movie['douban_id'] = str(i)
#     if movie:
#         db_helper.insert_movie(movie)
#
#     Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)

# 释放资源
movie_parser = None
db_helper.close_db()
