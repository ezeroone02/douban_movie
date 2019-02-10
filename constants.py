# coding=utf-8
# author=XingLong Pan
# date=2016-12-04

# 豆瓣电影的登录入口页面
DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

# 搜索引擎（SEO爬虫）的请求头
USER_AGENT = [
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
        'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
    ]
AGENT_SIZE = 7

# 延时设置
DELAY_MIN_SECOND = 1
DELAY_MAX_SECOND = 1.5

# 豆瓣电影的url前缀
URL_PREFIX = 'https://movie.douban.com/subject/'

DATA_PATH = 'data'
RATIO_POSTER_PATH = 'data\\ratio_poster\\'

"""
这里用到了阿布云代理动态版。使用影梭或者其他代理，甚至不用代理也可以
"""
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H6O0TPY9D5H9TM5D"
proxyPass = "82F8FD279973D68C"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

