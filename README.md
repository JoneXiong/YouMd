# YouMd
基于 [Editor.md](https://github.com/pandao/editor.md) 的MarkDown在线书写工具，很方便在本地/局域网/服务器快速运行，即时保存，在线管理

# 特性
* 快速便捷地运行，拿来即用
* 即时保存到本地客户端，一键发布到目录
* 无数据库，纯文档化，在线管理和查阅

# 使用
运行：
python server.py

访问：
首页 http://localhost:8081/

编辑器 http://localhost:8081/new

在线示例 [www.oejia.net](http://www.oejia.net/)


# 说明
发布保存的文档默认以.md存放在raw/entry/目录下

可配置的地方如下：
* config.py 配置一些常量、路径等
* templates/layout/ 配置站点头部、尾部及主菜单

页面上点edit图标即可直接进入编辑修改


# 定位
拿来即用的MarkDown编辑器；

如果你愿意它会是一个不错的轻博客系统（纯文档化）；

如果你想到了，它也可以是便捷的团队文档wiki系统

Screenshots
========
![info](https://github.com/JoneXiong/YouMd/raw/master/static/img/editor.png)

![info](https://github.com/JoneXiong/YouMd/raw/master/static/img/blog.jpg)

![info](https://github.com/JoneXiong/YouMd/raw/master/static/img/publish.jpg)

![data](https://github.com/JoneXiong/YouMd/raw/master/static/img/update.jpg)

# 计划
- ~~加入管理权限验证~~[已完成]
- 增加对团队多人发布与检索的支持
- ~~增加私人文档的支持，可过后选择发布~~[已完成]
- ~~增加图片上传及插入的支持~~
- 加入跟丰富多样的wiki组织形式
- 加入验证码功能


# Change log

### v1.1.0

- 加入简单用户登录验证与权限控制，支持更方便的在线管理
- 完善档案在线删除等管理功能
- 增加私密档案类别的支持，方便临时保存而不发布到站点
- 增加robots、sitemap等，方便搜索引擎收录
- 其他问题修复修复与优化

### v1.2.0

- 增加服务运行参数解析
- 图片上传与插入的支持
- 代码区显示优化
- 修复TOC锚点链接偏移问题
- 修复中文搜索不出的问题
