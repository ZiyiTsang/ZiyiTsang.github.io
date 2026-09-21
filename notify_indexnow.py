#!/usr/bin/env python3
"""
简单的IndexNow通知脚本
直接运行此脚本来通知IndexNow搜索引擎
"""

import json
import requests
import sys

def notify_indexnow():
    """发送IndexNow通知"""
    
    # API配置
    api_key = "9b818f8814e64eabb16c50d91332e2e8"
    host = "ziyitsang.github.io"
    api_url = "https://api.indexnow.org/indexnow"
    
    # 要通知的URL列表
    url_list = [
        "https://ziyitsang.github.io/",
        "https://ziyitsang.github.io/publications.html",
        "https://ziyitsang.github.io/projects_experience.html",
        "https://ziyitsang.github.io/showcase.html",
        "https://ziyitsang.github.io/more.html"
    ]
    
    # 构造请求数据
    payload = {
        "host": host,
        "key": api_key,
        "keyLocation": f"https://{host}/{api_key}.txt",
        "urlList": url_list
    }
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "IndexNow-Python-Script/1.0"
    }
    
    print("正在发送IndexNow通知...")
    print(f"主机: {host}")
    print(f"API密钥: {api_key}")
    print(f"密钥位置: {payload['keyLocation']}")
    print(f"URL数量: {len(url_list)}")
    print("\n发送的URL:")
    for i, url in enumerate(url_list, 1):
        print(f"  {i}. {url}")
    
    try:
        # 发送POST请求
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        print(f"\n=== 请求详情 ===")
        print(f"方法: POST")
        print(f"URL: {api_url}")
        print(f"Content-Type: {headers['Content-Type']}")
        print(f"Host: api.indexnow.org")
        print(f"\n请求体:")
        print(json.dumps(payload, indent=2))
        
        print(f"\n=== 响应结果 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        # IndexNow API返回200或202都表示成功
        if response.status_code in [200, 202]:
            print(f"\n✅ IndexNow通知发送成功！状态码: {response.status_code}")
            print("📝 注意: 202状态码表示请求已接受，搜索引擎将处理您的URL")
            return 0
        else:
            print(f"\n❌ IndexNow通知发送失败，状态码: {response.status_code}")
            return 1
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(notify_indexnow())