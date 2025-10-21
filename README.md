# Pelican 静态博客项目

一个基于 Pelican 静态网站生成器构建的 Python 博客项目。

## 项目简介

本项目使用 Pelican 静态网站生成器创建，支持 Markdown 和 reStructuredText 格式的文章编写，能够快速生成高性能的静态博客网站。

## 功能特性

- 🚀 基于 Pelican 静态网站生成器
- 📝 支持 Markdown 和 reStructuredText 格式
- 🎨 可自定义主题和样式
- 📱 响应式设计
- 🔍 支持搜索引擎优化
- 📊 Google Analytics 集成支持
- 💬 评论系统集成支持
- 🔖 标签和分类管理

## 环境要求

- Python 3.7+
- Pelican 4.8+
- Markdown 3.3+

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/lg2465214486/pelican_blog/
cd pelican-blog
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装 Pelican：

```bash
pip install pelican markdown
```

## 项目结构

```
pelican-blog/
├── content/              # 文章内容目录
│   ├── articles/        # 文章文件
│   └── images/           # 静态文件
├── output/              # 生成的静态文件
├── themes/              # 主题目录
├── pelicanconf.py       # 主配置文件
├── publishconf.py       # 发布配置文件
└── tasks.py             # 自动化任务脚本
```

## 使用方法

### 开发模式

```bash
# 生成网站并启动本地服务器
pelican content -s pelicanconf.py
pelican --listen
```

访问 http://localhost:8000 查看网站。

### 编写新文章

在 `content/articles/` 目录下创建 `.md` 或 `.rst` 文件：

```markdown
Title: 我的第一篇博客文章
Date: 2024-01-01 10:00
Category: Python
Tags: pelican, python, 博客
Slug: my-first-post

这是我的第一篇博客文章，使用 Pelican 生成！
```

### 构建生产版本

```bash
pelican content -s publishconf.py
```

## 配置说明

主要配置文件 `pelicanconf.py` 包含以下重要设置：

```python
# 站点信息
SITENAME = '我的博客'
SITEURL = ''
AUTHOR = '你的名字'

# 路径设置
PATH = 'content'
ARTICLE_PATHS = ['articles']
PAGE_PATHS = ['pages']

# 主题设置
THEME = 'themes/default'

# 插件设置
PLUGIN_PATHS = ['plugins']
PLUGINS = []

# 其他设置
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh'
```

## 部署

### GitHub Pages

```bash
# 构建生产版本
pelican content -s publishconf.py

# 部署到 GitHub Pages
ghp-import output -b gh-pages
git push origin gh-pages
```

### Netlify

将 `output` 目录部署到 Netlify，或配置构建命令：

```yaml
build_command: pelican content -s publishconf.py
publish_directory: output
```

### 其他平台

生成的静态文件位于 `output` 目录，可部署到任何静态网站托管服务。

## 自定义主题

1. 在 `themes/` 目录下创建新主题
2. 参考 Pelican 官方文档创建模板文件
3. 在配置文件中设置新主题：

```python
THEME = 'themes/your-theme-name'
```

## 插件使用

1. 将插件放置在 `plugins/` 目录
2. 在配置文件中启用插件：

```python
PLUGINS = ['plugin-name']
```

## 常用命令

```bash
# 快速创建新文章
pelican-quickstart

# 实时预览（开发模式）
pelican --autoreload --listen

# 清理生成的文件
pelican --delete-output-directory

# 重新生成所有文件
pelican content -s pelicanconf.py -d
```