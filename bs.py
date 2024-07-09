import requests
from tqdm import tqdm
import os
import json
import re
import time
import random


# 设置请求头
headers = {
    'Cookie': 'BDqhfp=%E9%99%B6%E7%93%B7%E6%9D%AF%26%260-10-1undefined%26%260%26%261; BAIDU_WISE_UID=wapp_1657077045994_41;',
    'Host': 'images.baidu.com',
    'Referer': 'https://images.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1718936722314_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=%E9%99%B6%E7%93%B7%E6%9D%AF',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}
number = 1
# 翻页
for page in range(1, 30):
    # 设置目标URL
    gsm = random.randint(0, 100)
    logid = random.randint(10000000000000000000, 99999999999999999999)
    url = f'https://images.baidu.com/search/acjson?tn=resultjson_com&logid={logid}&ipn=rj&ct=201326592&is=&fp=result&fr=&word=%E6%B0%B4%E6%9D%AF&queryWord=%E6%B0%B4%E6%9D%AF&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page * 30}&rn=30&gsm={gsm}'
    # 发送请求
    try:
        response = requests.get(url=url, headers=headers)
        time.sleep(1)
        response.raise_for_status()  # 检查响应是否有错误状态码
        print("请求成功！状态码为：", response.status_code)
        # 设置响应编码为 UTF-8
        response.encoding = 'utf-8'
        # 修复响应中的无效转义字符
        fixed_text = re.sub(r'\\(?=[^"\\/bfnrt])', r'\\\\', response.text)
        data_json = json.loads(fixed_text)

    except requests.exceptions.RequestException as e:
        print(f"请求失败或出现异常：{e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        print(f"响应内容: {response.text}")

    # 提取数据
    data_list = data_json['data']

    # 创建目标文件夹（如果不存在）
    os.makedirs('./bottle_data/cup', exist_ok=True)

    print('正在下载：')
    for data in data_list[:-1]:
        # 检查是否有有效的 hoverURL
        hoverURL = data.get('hoverURL')
        if hoverURL:
            print(f"下载URL: {hoverURL}")

            # 请求图片
            try:
                image_response = requests.get(hoverURL, stream=True)
                image_response.raise_for_status()
            except requests.RequestException as e:
                print(f"下载图片时出错：{e}")
                continue  # 跳过下载失败的图片

            # 获取图片大小
            total_size = int(image_response.headers.get('content-length', 0))
            file_path = f'./bottle_data/cup/{number}.jpeg'

            # 下载图片并更新进度条
            with open(file_path, mode='wb') as f:
                with tqdm(
                        desc=f'Downloading {number}',
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                ) as bar:
                    for chunk in image_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

            number += 1
