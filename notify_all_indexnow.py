#!/usr/bin/env python3
"""
从sitemap.xml读取所有URL并发送IndexNow通知
"""

import json
import requests
import sys
import xml.etree.ElementTree as ET

def parse_sitemap():
    """解析sitemap.xml，提取所有URL"""
    try:
        tree = ET.parse("sitemap.xml")
        root = tree.getroot()
        
        # 注册命名空间
        ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        urls = []
        
        # 尝试多种方式查找URL
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        url_elements = root.findall('.//ns:url', namespace)
        
        if not url_elements:
            url_elements = root.findall('.//url')
            
            if not url_elements:
                url_elements = [elem for elem in root.iter() if elem.tag.endswith('url')]
        
        # 提取loc元素
        for url in url_elements:
            loc = None
            if namespace:
                loc = url.find('.//ns:loc', namespace)
            
            if loc is None:
                loc = url.find('.//loc')
            
            if loc is None:
                for child in url:
                    if child.tag.endswith('loc'):
                        loc = child
                        break
            
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
        
        return urls
        
    except Exception as e:
        print(f"解析sitemap时出错: {str(e)}")
        return []

def notify_indexnow(urls):
    """发送IndexNow通知"""
    
    # API配置
    api_key = "5a933d53056640af8bee125d8f287aa5"
    host = "ziyitsang.github.io"
    api_url = "https://api.indexnow.org/indexnow"
    
    # 构造请求数据
    payload = {
        "host": host,
        "key": api_key,
        "keyLocation": f"https://{host}/{api_key}.txt",
        "urlList": urls
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
    print(f"URL数量: {len(urls)}")
    
    # 显示前10个URL作为示例
    print("\n部分URL列表:")
    for i, url in enumerate(urls[:10], 1):
        print(f"  {i}. {url}")
    if len(urls) > 10:
        print(f"  ... 还有 {len(urls) - 10} 个URL")
    
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

def main():
    """主函数"""
    print("=== IndexNow 通知工具 ===")
    
    # 解析sitemap获取URL
    urls = parse_sitemap()
    
    if not urls:
        print("❌ 未能从sitemap.xml中提取任何URL")
        return 1
    
    # 发送通知
    return notify_indexnow(urls)

if __name__ == "__main__":
    sys.exit(main())