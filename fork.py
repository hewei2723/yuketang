# -*- coding: utf-8 -*-
# version 1.0
# developed by zk chen
#原地址请看readme
#二次修改 hewei2723
#此源码适用于长江雨课堂

import time
import requests
import re
import base64
import json
CSR = "pP0cdp3DTR6lP5vQXrRMoOuM8aIsgd6E"
SES = "lru2o16nj32p52qoz3o0wubcenwews3u"
token = "5q2k5Li65byA5rqQ5bel5YW355SxaGV3ZWkyNzIz5LqM5qyh5byA5Y+R77yM5LuF5L6b5a2m5Lmg5Lqk5rWB5L2/55So"
print(base64.b64decode(token).decode())
csrftoken =  (CSR)
sessionid =  (SES)
select = True 
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',#UA设置
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=3078; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': '3078',
    'xtbz': 'cloud'
}

leaf_type = {
    "video": 0,
    "homework": 6,
    "exam": 5,
    "recommend": 3,
    "discussion": 4
}

课程id = []
章节map = {}
def one_video_watcher(video_id,video_name,cid,user_id,classroomid,skuid):
    video_id = str(video_id)
    classroomid = str(classroomid)
    url = "https://changjiang.yuketang.cn/video-log/heartbeat/"
    get_url = "https://changjiang.yuketang.cn/video-log/get_video_watch_progress/?cid="+str(cid)+"&user_id="+user_id+"&classroom_id="+classroomid+"&video_type=video&vtype=rate&video_id=" + str(video_id) + "&snapshot=1&term=latest&uv_id=3078"
    progress = requests.get(url=get_url, headers=headers)
    if_completed = '0'
    try:
        if_completed = re.search(r'"completed":(.+?),', progress.text).group(1)
    except:
        pass
    if if_completed == '1':
        print(video_name+"已经学习完毕，跳过")
        return 1
    else:
        print(video_name+"，尚未学习，现在开始自动学习")
    video_frame = 0
    val = 0
    learning_rate = 20
    t = time.time()
    timestap = int(round(t * 1000))
    while val != "1.0" and val != '1':
        heart_data = []
        for i in range(50):
            heart_data.append(
                {
                    "i": 5,
	                "et": "loadeddata",
	                "p": "web",
	                "n": "ali-cdn.xuetangx.com",
	                "lob": "ykt",
                    "cp": video_frame,
                    "fp": 0,
                    "tp": 0,
                    "sp": 1,
                    "ts": str(timestap),
                    "u": int(user_id),
                    "uip": "",
                    "c": cid,
                    "v": int(video_id),
                    "skuid": skuid,
                    "classroomid": classroomid,
                    "cc": video_id,
                    "d": 4976.5,
                    "pg": "4512143_tkqx",
                    "sq": 2,
                    "t": "video",
                    "cards_id": 0,
	                "slide": 0,
	                "v_url": ""
                }
            )
            video_frame += learning_rate
            max_time = int((time.time() + 3600) * 1000)
            timestap = min(max_time, timestap+1000*15)
        data = {"heart_data": heart_data}
        r = requests.post(url=url,headers=headers,json=data)
        # print(r.text)
        try:
            error_msg = json.loads(r.text)["message"]
            if "anomaly" in error_msg:
                video_frame = 0
        except:
            pass
        try:
            delay_time = re.search(r'Expected available in(.+?)second.', r.text).group(1).strip()
            print("由于网络阻塞，万恶的雨课堂，要阻塞" + str(delay_time) + "秒")
            time.sleep(float(delay_time) + 0.5)
            video_frame = 0
            print("恢复工作啦～～")
            submit_url = "https://changjiang.yuketang.cn/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=3078"
            r = requests.post(url=submit_url, headers=headers, data=data)
        except:
            pass
        progress = requests.get(url=get_url,headers=headers)
        tmp_rate = re.search(r'"rate":(.+?)[,}]',progress.text)
        if tmp_rate is None:
            return 0
        val = tmp_rate.group(1)
        print("学习进度为：" + str(float(val)*100) + "%/100%" + " last_point: " + str(video_frame))
        time.sleep(0.7)
    print("视频"+video_id+" "+video_name+"学习完成！")
    return 1

if __name__ == "__main__":
    # 获取userid
    response = requests.get('https://changjiang.yuketang.cn/v2/api/web/userinfo', headers=headers).text
    user_id = re.search(r'"user_id":(.*?),', response).group(1)
    params = {
        'identity': '2',
    }
    response = requests.get('https://changjiang.yuketang.cn/v2/api/web/courses/list', params=params,headers=headers).json()
    if response['errmsg'] != 'Success':
        print("csrftoken或者sessionid有问题请检查！")
        exit(1)
    index = 0
    # 获取课程id 和 课程名字
    for i in response['data']['list']:
        课程id.append(i['classroom_id'])
        print("编号：" + str(index + 1) + " 课名：" + str(i["course"]['name']))
        index += 1
    number = int(input("你想刷哪门课呢？请输入编号：\n"))
    cid = str(课程id[number-1])
    url = 'https://changjiang.yuketang.cn/v2/api/web/logs/learn/%s?actype=-1&page=0&offset=20&sort=-1'% cid
    response = requests.get(url,headers=headers).json()
    if response['data']['prev_id'] == -1:
        print('该课程尚无内容！程序退出....')
        exit(1)
    if response['errcode'] != 0:
        print(response)
        exit(1)
    courseware_id = []
    for i in response['data']['activities']:
        courseware_id.append(i['courseware_id'])
        章节map[i['courseware_id']] = i['title']
    data = {
        'cid': cid,
        'new_id':courseware_id
    }

    headers['classroom-id'] = cid
    headers['xtbz'] = 'ykt'
    headers['Referer'] = 'https://changjiang.yuketang.cn/v2/web/studentLog/%s'%cid
    if select:
        skuid = requests.get(url='https://changjiang.yuketang.cn/v2/api/web/classrooms/%s?role=5' % cid,
                             headers=headers).json()['data']['free_sku_id']
        get_url = 'https://changjiang.yuketang.cn/c27/online_courseware/schedule/score_detail/single/%s/0/' % skuid
        ret = requests.get(url=get_url, headers=headers).json()
        for i in ret['data']['leaf_level_infos']:
                get_url = 'https://changjiang.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/%s/%s/' % (cid, i['id'])
                getccid = requests.get(url=get_url, headers=headers).json()
                skuid = getccid['data']['sku_id']
                user_id = getccid['data']['user_id']
                ccid = getccid['data']['content_info']['media']['ccid']
                course_id = getccid['data']['course_id']
        one_video_watcher(i['id'], i['leaf_chapter_title'], course_id, str(user_id), cid, skuid)
        print("---------------------------已完成-------------------------------")
        for i in response['data']:
            if response['data'][i]['total_done'] == 1:
                print("%s已完成，跳过...."%章节map[i])
                continue
            url = 'https://changjiang.yuketang.cn/c27/online_courseware/xty/kls/pub_news/%s/'%i
            # # 只刷视频，练习跳过
            ret = requests.get(url, headers=headers).json()
            for j in ret['data']['content_info'][0]['section_list']:
                VideoId = j['leaf_list'][0]['id']
                get_url = 'https://changjiang.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/%s/%s/'%(cid,VideoId)
                getccid = requests.get(url=get_url,headers=headers).json()
                skuid = getccid['data']['sku_id']
                user_id = getccid['data']['user_id']
                ccid = getccid['data']['content_info']['media']['ccid']
                course_id = getccid['data']['course_id']
                one_video_watcher(VideoId,j['name'],course_id,str(user_id),cid,skuid)
            print("%s已完成...." % 章节map[i])
