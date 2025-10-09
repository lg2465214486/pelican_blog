# -*- coding: utf-8 -*-
from datetime import datetime

# 基本站点信息
AUTHOR = 'shiyi'
SITENAME = 'shiyi的博客'
SITEURL = ''  # 开发时留空，生产环境设置为你的域名

# 内容路径
PATH = "content"

# 时区和语言设置
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh'

# 主题设置
THEME = 'themes/bootstrap'  # 默认主题，可以更改为其他主题如 'flex', 'attila' 等

# 开发时禁用缓存设置
CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True  # 每次构建前清空输出目录

# 开发时启用相对URL（便于本地预览）
RELATIVE_URLS = True

# 开发时通常不需要Feed生成
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# 文章设置
DEFAULT_PAGINATION = 10  # 每页显示文章数量
DEFAULT_DATE = 'fs'  # 使用文件系统日期作为默认日期
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'  # 日期格式

# 目录设置
USE_FOLDER_AS_CATEGORY = True  # 使用文件夹作为分类
DISPLAY_CATEGORIES_ON_MENU = True  # 在菜单中显示分类
DISPLAY_PAGES_ON_MENU = True  # 在菜单中显示页面

# 静态文件路径
STATIC_PATHS = [
    'images',
    'extra'  # 用于存放CNAME、robots.txt等文件
]

# 额外文件配置
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# 友情链接
LINKS = (
    ("Pelican官方文档", "https://getpelican.com/"),
    ("Python官网", "https://www.python.org/"),
    ("本站源码", "https://github.com/lg2465214486/pelican_blog"),
)

# 社交媒体链接
SOCIAL = (
    ("GitHub", "https://github.com/lg2465214486"),
    ("Twitter", "https://twitter.com/yourusername"),
    ("知乎", "https://www.zhihu.com/people/yourusername"),
)

# URL 设置
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'

# 插件设置（如果需要）
PLUGIN_PATHS = ['plugins']  # 插件路径
PLUGINS = []  # 启用的插件列表

# Markdown扩展
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.meta': {},
        'markdown.extensions.admonition': {},
        # 添加图片处理扩展
        'markdown.extensions.attr_list': {},
        'markdown.extensions.toc': {'permalink': True},
    },
    'output_format': 'html5',
}

# 代码高亮设置
PYGMENTS_STYLE = 'monokai'

# 搜索引擎优化设置
SUMMARY_MAX_LENGTH = 70  # 摘要最大长度

# 开发调试设置
DEBUG = True  # 开发时启用调试模式