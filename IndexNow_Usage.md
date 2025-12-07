# IndexNow Python 命令使用指南

## 快速使用

您现在可以使用以下Python命令来通知IndexNow搜索引擎：

## 1. 通知主要页面（推荐用于快速测试）

```bash
python notify_indexnow.py
```

此脚本会通知以下主要页面：
- 首页
- 出版物页面
- 项目经验页面
- 展示页面
- 更多页面

## 2. 通知所有页面（完整通知）

```bash
python notify_all_indexnow.py
```

此脚本会：
1. 从 `sitemap.xml` 中读取所有URL
2. 向IndexNow发送完整的通知

## 请求格式示例

这些脚本发送的HTTP请求格式如下：

```http
POST /IndexNow HTTP/1.1
Content-Type: application/json; charset=utf-8
Host: api.indexnow.org

{
  "host": "ziyitsang.github.io",
  "key": "5a933d53056640af8bee125d8f287aa5",
  "keyLocation": "https://ziyitsang.github.io/5a933d53056640af8bee125d8f287aa5.txt",
  "urlList": [
    "https://ziyitsang.github.io/",
    "https://ziyitsang.github.io/publications.html",
    "https://ziyitsang.github.io/projects_experience.html",
    ...
  ]
}
```

## 输出示例

运行脚本后，您将看到类似以下的输出：

```
正在发送IndexNow通知...
主机: ziyitsang.github.io
API密钥: 5a933d53056640af8bee125d8f287aa5
密钥位置: https://ziyitsang.github.io/5a933d53056640af8bee125d8f287aa5.txt
URL数量: 30

部分URL列表:
  1. https://ziyitsang.github.io/
  2. https://ziyitsang.github.io/publications.html
  3. https://ziyitsang.github.io/projects_experience.html
  ...

=== 请求详情 ===
方法: POST
URL: https://api.indexnow.org/indexnow
Content-Type: application/json; charset=utf-8
Host: api.indexnow.org

=== 响应结果 ===
状态码: 200
响应内容: OK

✅ IndexNow通知发送成功！
```

## 何时使用

### 使用 `notify_indexnow.py` 当：
- 您只更新了主要页面
- 想要快速测试IndexNow功能
- 不需要通知所有页面

### 使用 `notify_all_indexnow.py` 当：
- 您进行了大量内容更新
- 想要确保所有页面都被通知
- 定期维护时使用

## 注意事项

1. 确保API密钥验证文件 `5a933d53056640af8bee125d8f287aa5.txt` 存在于网站根目录
2. 脚本需要安装 `requests` 库：`pip install requests`
3. 成功的通知会返回HTTP 200状态码
4. IndexNow会自动将您的URL提交给参与的搜索引擎

## 自动化集成

除了手动运行这些脚本，您的网站还配置了GitHub Actions自动通知：

- 内容更新时自动触发
- 每周定期运行
- 可手动触发完整通知

详细配置请参考 `SETUP_INDEXNOW.md` 文件。