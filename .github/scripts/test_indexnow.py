#!/usr/bin/env python3
"""
IndexNow 测试脚本
用于在本地测试IndexNow通知功能
"""

import os
import sys
import json
from datetime import datetime

# 添加脚本目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from indexnow import IndexNowNotifier

def test_sitemap_parsing():
    """测试sitemap解析功能"""
    print("=== 测试sitemap解析 ===")
    
    try:
        notifier = IndexNowNotifier("test_key", "https://ziyitsang.github.io")
        urls = notifier.parse_sitemap("sitemap.xml")
        
        if urls:
            print(f"✅ 成功解析sitemap，找到 {len(urls)} 个URL")
            print("前5个URL:")
            for i, url in enumerate(urls[:5]):
                print(f"  {i+1}. {url}")
            return True
        else:
            print("❌ 未能从sitemap中解析出任何URL")
            return False
            
    except Exception as e:
        print(f"❌ 解析sitemap时出错: {str(e)}")
        return False

def test_api_key_file():
    """测试API密钥验证文件"""
    print("\n=== 测试API密钥验证文件 ===")
    
    api_key = "5a933d53056640af8bee125d8f287aa5"
    key_file = f"{api_key}.txt"
    
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                content = f.read().strip()
            
            if content == api_key:
                print(f"✅ API密钥验证文件 {key_file} 存在且内容正确")
                return True
            else:
                print(f"❌ API密钥验证文件 {key_file} 内容不匹配")
                return False
                
        except Exception as e:
            print(f"❌ 读取API密钥验证文件时出错: {str(e)}")
            return False
    else:
        print(f"❌ API密钥验证文件 {key_file} 不存在")
        return False

def test_notification_dry_run():
    """测试通知功能（干运行，不实际发送API请求）"""
    print("\n=== 测试通知功能（干运行）===")
    
    try:
        api_key = os.environ.get('INDEXNOW_API_KEY', '5a933d53056640af8bee125d8f287aa5')
        notifier = IndexNowNotifier(api_key, "https://ziyitsang.github.io")
        
        # 解析sitemap获取URL
        urls = notifier.parse_sitemap("sitemap.xml")
        
        if not urls:
            print("❌ 没有URL可以测试")
            return False
        
        # 只测试前3个URL
        test_urls = urls[:3]
        print(f"将测试通知以下URL（仅显示，不实际发送）:")
        for i, url in enumerate(test_urls):
            print(f"  {i+1}. {url}")
        
        # 构造请求数据（不实际发送）
        payload = {
            "host": "ziyitsang.github.io",
            "key": api_key,
            "keyLocation": f"https://ziyitsang.github.io/{api_key}.txt",
            "urlList": test_urls
        }
        
        print(f"✅ 请求数据构造成功")
        print(f"  主机: {payload['host']}")
        print(f"  密钥位置: {payload['keyLocation']}")
        print(f"  URL数量: {len(payload['urlList'])}")
        
        # 保存测试数据到文件
        with open('indexnow_test_payload.json', 'w') as f:
            json.dump(payload, f, indent=2)
        print("✅ 测试数据已保存到 indexnow_test_payload.json")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试通知功能时出错: {str(e)}")
        return False

def main():
    """主测试函数"""
    print(f"IndexNow 集成测试 - {datetime.now().isoformat()}")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_sitemap_parsing,
        test_api_key_file,
        test_notification_dry_run
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 时发生异常: {str(e)}")
            results.append(False)
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("=== 测试结果摘要 ===")
    print(f"总测试数: {len(results)}")
    print(f"通过测试: {sum(results)}")
    print(f"失败测试: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 所有测试通过！IndexNow集成配置正确。")
        print("\n下一步:")
        print("1. 确保在GitHub仓库中设置了INDEXNOW_API_KEY Secret")
        print("2. 推送一些内容更改来触发GitHub Actions工作流")
        print("3. 在Actions页面检查工作流运行结果")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查上述错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())