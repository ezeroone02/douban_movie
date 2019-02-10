# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import time
import random
import constants
import requests
import logging

from utils import ForbiddenError


class Utils:

    @staticmethod
    def delay(min_second, max_second):
        time.sleep(random.uniform(min_second, max_second))

    @staticmethod
    def request_and_parse_movies(id_list, movie_parser, db_helper, cookies):
        logging.info("request_and_parse_movies log")
        # 通过ID进行遍历
        for i in id_list:

            headers = {'User-Agent': random.choice(constants.USER_AGENT)}

            # 获取豆瓣页面(API)数据
            r = requests.get(
                constants.URL_PREFIX + str(i),
                headers=headers,
                cookies=cookies,
                proxies=constants.proxies
            )
            r.encoding = 'utf-8'
            if r.status_code == '403':
                print(constants.URL_PREFIX + str(i) + "403")
                raise ForbiddenError
                break
            # 提示当前到达的id(log)
            print('id: ' + str(i))

            # 提取豆瓣数据
            movie_parser.set_html_doc(r.text)
            movie = movie_parser.extract_movie_info()

            # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
            if not movie:
                Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
                continue

            # 豆瓣数据有效，写入数据库
            movie['douban_id'] = str(i)
            if movie:
                db_helper.insert_movie(movie)

            image_name = constants.RATIO_POSTER_PATH + "%s.jpg" % i
            # 下载图片并保存到当前目录
            ratio_poster_image = open(image_name, 'wb')
            retio_poster_request = requests.get(movie['ratio_poster'])
            ratio_poster_image.write(retio_poster_request.content)
            ratio_poster_image.close()
            retio_poster_request.close()
            logging.info(str(i)+" DONE")
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)

    @staticmethod
    def mkdir(path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print(path + ' 创建成功')
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False
