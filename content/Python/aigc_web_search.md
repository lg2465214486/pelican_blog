Title: deepseek实现深度网搜
Date: 2025-10-15 17:00
Modified: 2025-10-15 17:00
Author: shiyi
tags: 源码,aigc
keywords: 以deepseek为基本模型，利用langchain构建提示词链实现以工作流形式分析搜索回答用户提问。
summary: 以deepseek为基本模型，利用langchain构建提示词链实现以工作流形式分析搜索回答用户提问。
lang: zh
status: published
Slug: aigc_web_search
url: aigc_web_search

<br>

# deepseek实现深度网搜

本文主要讲述如何使用deepseek为基础模型，调用百度搜索api实现，利用python的aigc框架 `langchain` ，编排提示词链实现深度网搜的全过程。

[langchain中文文档网站](https://python.langchain.com.cn/)

流程图如下：

[![图1]({static}/images/aigc_web_search/1.png){: width="70%"}]({static}/images/aigc_web_search/1.png){: data-lightbox="gallery" .lightbox-image }

图中每一个chain都代表一个和AI交互的全过程

**节点描述**：

`chain1`：分析用户输入的问题节点，利用ai对出用户输入的问题本质进行提炼。

`chain2`：根据chain1提炼后的内容，利用ai生成搜索策略关键词。

`chain3`：利用AI，结合用户的提问，对搜索到的结果整理提炼，排除重复以及干燥的搜索结果。

`chain4`：利用AI，结合用户的提问，对chain3整理提炼的内容进行深度分析，分析信息维度侧重点。

`chain5`：利用AI，结合用户的提问，结合chain3、chain4的结果，构建完整的深度搜索回答。

<br>

由于代码行数较多，页面就不放源码了，源码已经上传到github上，感兴趣的朋友自行下载。

[github源码地址](https://github.com/lg2465214486/tools/blob/main/python/aigc/langchain_web_seach.py)

运行结果：

[![图1]({static}/images/aigc_web_search/2.png){: width="50%"}]({static}/images/aigc_web_search/2.png){: data-lightbox="gallery" .lightbox-image }

[![图1]({static}/images/aigc_web_search/3.png){: width="50%"}]({static}/images/aigc_web_search/3.png){: data-lightbox="gallery" .lightbox-image }

<br>

<br>

### 免责声明

> **本文为技术研究目的撰写，仅供学习交流。**

1.  **内容时效性**： 技术信息具有时效性，本文内容发布后可能已过时，请自行验证。
2.  **使用风险自担**： 应用本文所述方法所产生的一切直接或间接后果，均由使用者自行承担。
3.  **合法合规使用**： **严禁**将本文内容用于任何违反法律法规或侵害他人权益的用途（如未经授权的爬虫、网络攻击、数据窃取等）。
4.  **版权声明**： 本文为原创内容，转载需注明出处。文中引用的第三方资源，其版权归原作者所有。