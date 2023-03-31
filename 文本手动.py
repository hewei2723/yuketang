import time
import webbrowser
for i in range(18, 30):
#这里是生成打开浏览器的页码
    webbrowser.open_new_tab('https://changjiang.yuketang.cn/v2/web/lms/填入你的/graph/166705%d' % i)
# 上述链接获取方法：登录雨课堂后点击你的课程，下面有图文课程，随便点一篇进去就是这个链接 166705%d这里的5是从5开头的文章，实际上从第一篇文章开始是4开头的，原理是访问400到500页的网页，酌情修改
    time.sleep(2)#运行一次睡两秒


