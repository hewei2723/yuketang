# -*- coding: utf-8 -*-
# version 4.1
# 此源码适用于长江雨课堂
import time
import requests
import re
import base64
import json
CSR = input("请输入你的CSR：")
SES = input("请输入你的SES：")
token = "5q2k5Li65byA5rqQ5bel5YW355SxaGV3ZWkyNzIz5LqM5qyh5byA5Y+R77yM5LuF5L6b5a2m5Lmg5Lqk5rWB5L2/55So"
csrftoken = (CSR)
sessionid = (SES)
select = True
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    # UA设置
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=3714; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': '3714',
    'xtbz': 'cloud'
}

leaf_type = {
    "video": 0,
    "homework": 6,
    "exam": 5,
    "recommend": 3,
    "discussion": 4
}

Classid = []
Unitmap = {}


def decode_token():
    token = "5q2k5Li65byA5rqQ5bel5YW355SxaGV3ZWkyNzIz5LqM5qyh5byA5Y+R77yM5LuF5L6b5a2m5Lmg5Lqk5rWB5L2/55So"
    print(base64.b64decode(token).decode())


def get_user_id():
    response = requests.get('https://changjiang.yuketang.cn/v2/api/web/userinfo', headers=headers).text
    return re.search(r'"user_id":(.*?),', response).group(1)


def get_course_list():
    params = {'identity': '2'}
    response = requests.get('https://changjiang.yuketang.cn/v2/api/web/courses/list', params=params,
                            headers=headers).json()
    if response['errmsg'] != 'Success':
        print("你的csrftoken或者sessionid填错了！")
        exit(1)

    index = 0
    for i in response['data']['list']:
        Classid.append(i['classroom_id'])
        print("编号：" + str(index + 1) + " 课名：" + str(i["course"]['name']))
        index += 1

    number = int(input("你学习哪节课？输入编号：\n"))
    return str(Classid[number - 1])


def get_video_watch_progress(cid, user_id, classroomid, video_id):
    url = f"https://changjiang.yuketang.cn/video-log/get_video_watch_progress/?cid={cid}&user_id={user_id}&classroom_id={classroomid}&video_type=video&vtype=rate&video_id={video_id}&snapshot=1&term=latest&uv_id=3714"
    progress = requests.get(url=url, headers=headers)
    return progress


def lookok(video_id, video_name, cid, user_id, classroomid, skuid):
    video_id = str(video_id)
    classroomid = str(classroomid)
    url = "https://changjiang.yuketang.cn/video-log/heartbeat/"
    get_url = f"https://changjiang.yuketang.cn/video-log/get_video_watch_progress/?cid={cid}&user_id={user_id}&classroom_id={classroomid}&video_type=video&vtype=rate&video_id={video_id}&snapshot=1&term=latest&uv_id=3714"
    progress = get_video_watch_progress(cid, user_id, classroomid, video_id)

    if_completed = '0'
    try:
        if_completed = re.search(r'"completed":(.+?),', progress.text).group(1)
    except:
        pass

    if if_completed == '1':
        print(video_name + " 这个已经学过了啊 ！你怎么能偷偷学习？")
        return 1
    else:
        print(video_name + "，正在迷惑服务器")

    video_frame = 0
    val = 0
    learning_rate = 20
    t = time.time()
    timestap = int(round(t * 1000))

    while val not in ["1.0", '1']:
        heart_data = []
        for i in range(65):
            heart_data.append({
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
                "d": 4981.0,
                "pg": "4512543_skdv",
                "sq": 2,
                "t": "video",
                "cards_id": 0,
                "slide": 0,
                "v_url": ""
            })
            video_frame += learning_rate
            max_time = int((time.time() + 3600) * 1000)
            timestap = min(max_time, timestap + 1000 * 15)

        data = {"heart_data": heart_data}
        r = requests.post(url=url, headers=headers, json=data)
        try:
            error_msg = json.loads(r.text)["message"]
            if "anomaly" in error_msg:
                video_frame = 0
        except:
            pass

        progress = get_video_watch_progress(cid, user_id, classroomid, video_id)
        tmp_rate = re.search(r'"rate":(.+?)[,}]', progress.text)
        if tmp_rate is None:
            return 0

        val = tmp_rate.group(1)
        print("当前学习进度为：" + str(float(val) * 100) + "%/100%" + " last_point: " + str(video_frame))
        time.sleep(0.7)

    print("视频" + video_id + " " + video_name + "学习完成！")
    return 1


if __name__ == "__main__":
    decode_token()
    user_id = get_user_id()
    cid = get_course_list()
    headers['classroom-id'] = cid
    headers['xtbz'] = 'ykt'
    headers['Referer'] = 'https://changjiang.yuketang.cn/v2/web/studentLog/%s' % cid

    if select:
        skuid = requests.get(url='https://changjiang.yuketang.cn/v2/api/web/classrooms/%s?role=5' % cid,
                             headers=headers).json()['data']['free_sku_id']
        get_url = 'https://changjiang.yuketang.cn/c27/online_courseware/schedule/score_detail/single/%s/0/' % skuid
        ret = requests.get(url=get_url, headers=headers).json()
        for i in ret['data']['leaf_level_infos']:
            if i['leaf_level_title'] != 'Video':
                get_url = 'https://changjiang.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/%s/%s/' % (cid, i['id'])
                getccid = requests.get(url=get_url, headers=headers).json()
                skuid = getccid['data']['sku_id']
                user_id = getccid['data']['user_id']
                ccid = getccid['data']['content_info']['media']['ccid']
                course_id = getccid['data']['course_id']
                lookok(i['id'], i['leaf_level_title'], course_id, str(user_id), cid, skuid)
        print("--偷懒吧你！--")
    else:
        response = requests.post('https://changjiang.yuketang.cn/mooc-api/v1/lms/learn/course/pub_new_pro',
                                 headers=headers, data=json.dumps(data)).json()
        for i in response['data']:
            if response['data'][i]['total_done'] == 1:
                print("%s你偷偷看了网课？，跳过...." % Unitmap[i])
                continue
            url = 'https://changjiang.yuketang.cn/c27/online_courseware/xty/kls/pub_news/%s/' % i
            ret = requests.get(url, headers=headers).json()
            for j in ret['data']['content_info'][0]['section_list']:
                VideoId = j['leaf_list'][0]['id']
                get_url = 'https://changjiang.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/%s/%s/' % (cid, VideoId)
                getccid = requests.get(url=get_url, headers=headers).json()
                skuid = getccid['data']['sku_id']
                user_id = getccid['data']['user_id']
                course_id = getccid['data']['course_id']
                lookok(VideoId, j['name'], course_id, str(user_id), cid, skuid)
            print("%sOK!...." % Unitmap[i])
