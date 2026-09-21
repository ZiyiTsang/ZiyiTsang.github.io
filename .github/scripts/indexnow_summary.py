#!/usr/bin/env python3
"""
IndexNow 结果摘要打印脚本

从 indexnow_result.json 读取结果并打印摘要。
本脚本始终以退出码 0 结束：摘要只是信息展示，
不应因为通知失败而让 CI 变红（外部服务不稳定是常态）。
"""

import json
import os
import sys

RESULT_FILE = "indexnow_result.json"


def main() -> int:
    if not os.path.exists(RESULT_FILE):
        print("[SKIP] 未找到结果文件 indexnow_result.json，跳过摘要")
        return 0

    try:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            result = json.load(f)
    except Exception as e:
        print(f"[SKIP] 结果文件解析失败: {e}")
        return 0

    total_urls = result.get("total_urls", 0)
    total_batches = result.get("total_batches", 0)
    successful_batches = result.get("successful_batches", 0)

    print("=== IndexNow 通知结果摘要 ===")
    print(f"总URL数: {total_urls}")
    print(f"总批次数: {total_batches}")
    print(f"成功批次: {successful_batches}")

    for item in result.get("results", []):
        status = item.get("status_code", "-")
        ok = item.get("success", False)
        print(f"  批次 {item.get('batch', '?')}: HTTP {status} -> {'成功' if ok else '失败'}")

    if total_batches == 0:
        print("[WARN] 没有任何批次被提交")
    elif successful_batches < total_batches:
        print("[WARN] 部分批次提交失败")
        print("       常见原因：密钥校验未通过（403 UserForbiddedToAccessSite）")
    else:
        print("[OK] 所有批次提交成功")

    return 0


if __name__ == "__main__":
    sys.exit(main())
