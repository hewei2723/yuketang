import requests
import time
import json

# 设置请求头和心跳包数据
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Content-Type": "application/json",
    "Referer": "https://changjiang.yuketang.cn/v2/web/xcloud/video-student/15024716/19899362",
    # 其他请求头...
}

cookies = {
    "csrftoken": "pP0cdp3DTR6lP5vQXrRMoOuM8aIsgd6E",
    "sessionid": "lru2o16nj32p52qoz3o0wubcenwews3u",
    "classroomId": "15024716",
    "classroom_id": "15024716",
    "django_language": "zh-cn",
    # 其他 cookies...
}

# 设置目标 URL
url = "https://changjiang.yuketang.cn/video-log/heartbeat/"

# 构造心跳包数据
def construct_heartbeat_data(completion, duration):
    return {
        "i": 5,
        "et": "playing",
        "p": "web",
        "n": "ali-cdn.xuetangx.com",
        "lob": "ykt",
        "cp": completion,
        "fp": 0,
        "tp": duration,
        "sp": 1,
        "ts": str(int(time.time() * 1000)),
        "u": 41951039,
        "uip": "",
        "c": 2587312,
        "v": 19899362,
        "skuid": 7091592,
        "classroomid": "15024716",
        "cc": "BCAAF795DA1168259C33DC5901307461",
        "d": 759.3,
        "pg": "19899362_17oad",
        "sq": completion,
        "t": "video",
        "cards_id": 0,
        "slide": 0,
        "v_url": ""
    }

# 发送心跳包
for i in range(101):
    heartbeat_data = construct_heartbeat_data(i, i)
    
    response = requests.post(url, headers=headers, cookies=cookies, json={"heart_data": [heartbeat_data]})

    # 检查响应
    if response.status_code == 200:
        print(f"心跳包发送成功 - 完成度: {i}%")
    else:
        print(f"心跳包发送失败 - 完成度: {i}%, 状态码: {response.status_code}")

    # 可以根据需要调整发送心跳包的时间间隔
    time.sleep(1)
