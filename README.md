# YouMd
基于 [Editor.md](https://github.com/pandao/editor.md) 的MarkDown在线书写工具，很方便在本地/局域网/服务器快速运行，即时保存，在线管理

# 特性
* 快速便捷地运行，拿来即用
* 即时保存到本地客户端，一键发布到目录
* 无数据库，纯文档化，在线管理和查阅
* 基于Git版本控制支持,记录文档历史修改记录
* 支持一键导出pdf文档

# 使用
运行：
`python server.py`

访问：
> 首页 http://localhost:8081/

> 编辑器 http://localhost:8081/new

在线示例 [www.oejia.net](http://www.oejia.net/)

# 专业版
- 性能提升数倍，支持更庞大的文档大小和数量
- 支持自定义首页
- 支付配置项控制是否所有页面需要登录才能访问
- 部署更简单，更好地支持本地 Windows 系统

联系我们 https://www.calluu.cn/page/contactus


# 说明
使用说明及文档: 
- [基本使用说明](http://www.oejia.net/blog/2016/02/23/youmd_base_use.html)
- [其他文档](http://www.oejia.net/search?type=category&value=YouMd&start=1&limit=5)

发布保存的文档默认以.md存放在raw/entry/目录下

可配置的地方如下：
* config.py 配置一些常量、路径等
* templates/layout/ 配置站点头部、尾部及主菜单

页面上点edit图标即可直接进入编辑修改

开启git支持需要先安装 GitPython 并在 config.py 中开启 use_git

默认开启了md内容中style,script,iframe等HTML标签的解析，需要调整可以编辑entry.html 改变 htmlDecode 配置项

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
- [x] 加入管理权限验证
- [x] 增加私人文档的支持，可过后选择发布
- [x] 增加图片上传及插入的支持
- [x] 加入更丰富多样的wiki组织形式
- [x] 增加对团队多人发布与检索的支持
- [ ] 加入验证码功能


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

### v1.3.0

- 细节修复完善
- 增加多用户支持
- 增加头信息管理功能

### v1.4.0

- 增加国际化的支持
- 增强全屏化的前端兼容性
- 优化session更新机制
- 私人档的多用户支持
- 优化分页样式效果和内容页样式

### v1.5.0

- 保存时增加快捷键支持
- 增加基于Git的版本控制支持（修改历史全记录）
- 风格优化，区块显示更清晰醒目
- 其他优化与问题修复


### v1.5.1
- 增加tag、category两个扩展标签的后台解析支持，用于快速引用标签和分类的列表链接
- 列表模式增加分类和标签的显示
- 增加一键(Ctrl+b)打印或导出pdf功能
- 编辑器增加快折叠的支持
- 其他问题修复与优化
