# -*- coding: utf-8 -*-
from pelicanconf import *

# 生产环境设置
SITEURL = 'https://yourdomain.com'  # 替换为你的实际域名
RELATIVE_URLS = False  # 生产环境使用绝对URL

# 启用Feed
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# 禁用调试模式
DEBUG = False

# 生产环境可以启用缓存
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True
DELETE_OUTPUT_DIRECTORY = False

# 搜索引擎优化
GOOGLE_ANALYTICS = 'UA-XXXXX-X'  # 你的Google Analytics ID