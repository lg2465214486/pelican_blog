Title: 某音视频信息抓取
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 工具,源码,干货
keywords: 某音App视频信息抓取
lang: zh
status: published
Slug: crawler-douyin-web1
url: crawler-douyin-web1

<br>
&emsp;&emsp;前几天，我接了个小项目，需要批量分析某音上的热门视频。我的第一反应当然是写个爬虫脚本，直接请求接口。然而，理想很丰满，现实很骨感——某音的反爬机制比我想象的还要严密，逆向的过程艰难无比，各种js加载器、循环跳转、动态生成的加密签名参数....

在当今的爬虫领域，对于像某音这样的大型App，获取数据的主流技术路径无非两条：

- 逆向分析派：深入剖析App或网页的JavaScript代码，还原核心加密参数（如**a-Bogus、__ac_signature、msToken**）的生成逻辑，直接在请求头中携带，实现高效抓取。

- 模拟浏览器派：通过工具直接控制一个真实的浏览器，所有的JS执行、参数生成、Cookie管理都由浏览器自动完成，程序只需“坐享其成”。

&emsp;&emsp;前者性能极高，是专业爬虫工程师的首选，但技术门槛高、维护成本大。而后者，以 Selenium 为代表，虽然速度稍慢，但其开发简单、绕过复杂加密、近乎于“无脑” 的优点，让它成为了快速原型、小规模数据抓取或个人开发者的绝佳选择。本文将详细讲解如何利用Selenium这条“捷径”，轻松抓取某音视频信息。


**我们要抓取一个页面上的数据，首先要先找到给页面提供数据的接口**

&emsp;&emsp;如下图，通过浏览器的开发者工具，在阅读完所有主要的网络请求后，我们发现其页面上的视频，图片，推文和博主信息都在一个名为 `v1/web/aweme/detail`的接口当中

[![图1]({static}/images/crawler-douyin-web/1.png){: width="100%"}]({static}/images/crawler-douyin-web/1.png){: data-lightbox="gallery" .lightbox-image }


<br>
&emsp;&emsp;我们能清楚的看到，在这个接口的后面携带了各种校验参数，如果通过逆向的方法必定要花费大量的时间精力，而且每次接口参数的加密规则发生了变化，又得重新逆向补环境...

Selenium抓取的原理：

利用Selenium自动打开页面-->监听页面所有请求-->匹配到`v1/web/aweme/detail`接口-->获取到此接口的所有Heads、参数-->重放此次请求

