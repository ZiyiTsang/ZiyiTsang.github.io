#!/usr/bin/env python3
"""
IndexNow API 通知脚本
用于在网站内容更新时通知搜索引擎
"""

import json
import sys
import xml.etree.ElementTree as ET
import requests
import os
import time
from datetime import datetime
from typing import List, Dict, Optional

class IndexNowNotifier:
    def __init__(self, api_key: str, base_url: str = "https://ziyitsang.github.io"):
        """
        初始化IndexNow通知器
        
        Args:
            api_key: IndexNow API密钥
            base_url: 网站基础URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.api_endpoint = "https://api.indexnow.org/indexnow"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'IndexNow-Python-Script/1.0'
        })
    
    def parse_sitemap(self, sitemap_path: str = "sitemap.xml") -> List[str]:
        """
        解析sitemap.xml文件，提取所有URL
        
        Args:
            sitemap_path: sitemap.xml文件路径
            
        Returns:
            URL列表
        """
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            
            # 注册命名空间
            ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            ET.register_namespace('image', 'http://www.google.com/schemas/sitemap-image/1.1')
            
            urls = []
            
            # 尝试多种方式查找URL
            # 方式1: 使用命名空间
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            url_elements = root.findall('.//ns:url', namespace)
            
            if not url_elements:
                # 方式2: 不使用命名空间
                url_elements = root.findall('.//url')
                
                if not url_elements:
                    # 方式3: 直接遍历所有元素
                    url_elements = [elem for elem in root.iter() if elem.tag.endswith('url')]
            
            # 提取loc元素
            for url in url_elements:
                # 尝试多种方式查找loc
                loc = None
                if namespace:
                    loc = url.find('.//ns:loc', namespace)
                
                if loc is None:
                    loc = url.find('.//loc')
                
                if loc is None:
                    # 直接查找子元素
                    for child in url:
                        if child.tag.endswith('loc'):
                            loc = child
                            break
                
                if loc is not None and loc.text:
                    urls.append(loc.text.strip())
            
            print(f"从sitemap中提取到 {len(urls)} 个URL")
            return urls
            
        except Exception as e:
            print(f"解析sitemap时出错: {str(e)}")
            return []
    
    def notify_indexnow(self, urls: List[str]) -> Dict[str, any]:
        """
        向IndexNow API发送通知
        
        Args:
            urls: 要通知的URL列表
            
        Returns:
            API响应结果
        """
        if not urls:
            return {"error": "没有URL需要通知"}
        
        # IndexNow API支持批量提交，但一次最多10,000个URL
        batch_size = 10000
        results = []
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            
            payload = {
                "host": self.base_url.replace('https://', '').replace('http://', ''),
                "key": self.api_key,
                "keyLocation": f"{self.base_url}/{self.api_key}.txt",
                "urlList": batch
            }
            
            try:
                print(f"正在提交第 {i//batch_size + 1} 批，包含 {len(batch)} 个URL")
                response = self.session.post(
                    self.api_endpoint,
                    json=payload,
                    timeout=30
                )
                
                result = {
                    "batch": i//batch_size + 1,
                    "status_code": response.status_code,
                    "response_text": response.text,
                    # IndexNow 成功时返回 200，或返回 202 表示已接受待处理
                    "success": response.status_code in (200, 202)
                }
                
                results.append(result)
                
                if result["success"]:
                    print(f"第 {i//batch_size + 1} 批提交成功 (HTTP {response.status_code})")
                else:
                    print(f"第 {i//batch_size + 1} 批提交失败: HTTP {response.status_code} - {response.text}")
                
                # 添加延迟以避免请求过于频繁
                if i + batch_size < len(urls):
                    time.sleep(1)
                    
            except requests.exceptions.RequestException as e:
                error_result = {
                    "batch": i//batch_size + 1,
                    "error": str(e),
                    "success": False
                }
                results.append(error_result)
                print(f"第 {i//batch_size + 1} 批提交异常: {str(e)}")
        
        return {
            "total_urls": len(urls),
            "total_batches": len(results),
            "successful_batches": sum(1 for r in results if r.get("success", False)),
            "results": results
        }
    
    def create_api_key_file(self, output_path: str = None):
        """
        创建API密钥验证文件
        
        Args:
            output_path: 输出文件路径，默认为根目录下的{api_key}.txt
        """
        if output_path is None:
            output_path = f"{self.api_key}.txt"
        
        try:
            with open(output_path, 'w') as f:
                f.write(self.api_key)
            print(f"已创建API密钥验证文件: {output_path}")
        except Exception as e:
            print(f"创建API密钥验证文件时出错: {str(e)}")

def main():
    """主函数"""
    # 从环境变量获取API密钥
    api_key = os.environ.get('INDEXNOW_API_KEY')
    if not api_key:
        print("错误: 未设置INDEXNOW_API_KEY环境变量")
        sys.exit(1)
    
    # 从命令行参数获取基础URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://ziyitsang.github.io"
    
    # 从命令行参数获取sitemap路径
    sitemap_path = sys.argv[2] if len(sys.argv) > 2 else "sitemap.xml"
    
    print(f"开始IndexNow通知流程 - {datetime.now().isoformat()}")
    print(f"基础URL: {base_url}")
    print(f"Sitemap路径: {sitemap_path}")
    
    # 初始化通知器
    notifier = IndexNowNotifier(api_key, base_url)
    
    # 创建API密钥验证文件
    notifier.create_api_key_file()
    
    # 解析sitemap
    urls = notifier.parse_sitemap(sitemap_path)
    if not urls:
        print("警告: 没有找到任何URL")
        sys.exit(0)
    
    # 发送通知
    result = notifier.notify_indexnow(urls)
    
    # 输出结果
    print("\n=== IndexNow通知结果 ===")
    print(f"总URL数: {result['total_urls']}")
    print(f"总批次数: {result['total_batches']}")
    print(f"成功批次: {result['successful_batches']}")
    
    # 保存结果到JSON文件
    with open('indexnow_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("详细结果已保存到 indexnow_result.json")
    
    # 如果有任何失败的批次，返回非零退出码
    if result['successful_batches'] < result['total_batches']:
        print("警告: 部分批次提交失败")
        sys.exit(1)
    else:
        print("所有批次提交成功")
        sys.exit(0)

if __name__ == "__main__":
    main()