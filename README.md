# 长江雨课堂刷网课 新乡工程学院雨课堂
用来刷网课，适用于长江雨课堂
# 长江雨课堂刷视频脚本

#### 介绍

项目1.0(fork.py)源自:https://github.com/heyblackC/yuketangHelper  不过已经不能用了

项目2.0(videookok.py) 1.0说是通过修改心跳包来达到刷课的目的，我在他的思路下重写了一份代码

此代码原生适配 新乡工程学院雨课堂

如使用Thony需要先安装requsets库
库地址 https://github.com/psf/requests
#### 注意

目前不可用于公选课，但可以尝试一下
### 2023.3.31更新
最近选课选到了影视鉴赏，发现里面有个图文模块，只需要打开那个页面就可以完成进度
，因为有100多篇，手动打开太复杂了，就写了个半自动脚本。
### 2023.11.24更新
好消息，我花了三天时间研究并重构了代码，现在可以用来刷公选课了
csrftoken和sessionid的获取方法，在edge或者chrome浏览器登录雨课堂后，按F12打开控制台，上面那一行有一个应用程序字样，在cookies里面复制就可以了。
### 2023.11.25更新
我发现换一个账户就不能用了，debug后发现cid（Classid = []）有问题，这个就是课程的实际编号，日志中的编号是生成的编号，所以编号和实际编号不一样导致获取到了其他的课程信息！

编号是跟老师上传课程顺序有关，举个例子，如果你的课程是 编号：4 课名：就业创业 如果你输入4没反应或者报错KeyError: 'ccid' ，就输入3或者5,也就是编号附近的数字，范围一般不会超过+-2
###
如果你用到了这份代码，请点一个小星星