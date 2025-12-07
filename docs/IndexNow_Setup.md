# IndexNow 集成指南

本文档说明如何使用和维护网站的IndexNow集成，以便在内容更新时自动通知搜索引擎。

## 什么是 IndexNow？

IndexNow 是一个由微软必应和雅虎发起的协议，允许网站所有者在内容更新时立即通知搜索引擎。这有助于搜索引擎更快地发现和索引您的新内容或更新内容。

## 工作原理

我们的IndexNow集成包含以下组件：

1. **Python脚本** (`.github/scripts/indexnow.py`): 负责解析sitemap.xml并向IndexNow API发送通知
2. **GitHub Actions工作流** (`.github/workflows/indexnow.yml`): 自动触发通知流程
3. **API密钥验证文件**: 验证您对网站的所有权

## 自动触发条件

IndexNow通知会在以下情况下自动触发：

1. **内容更新时**: 当以下类型的文件被推送到main/master分支时
   - Markdown文件 (`.md`)
   - HTML文件 (`.html`)
   - YAML配置文件 (`.yml`, `.yaml`)
   - 内容目录中的文件 (`_posts/`, `_publications/`, `_news/`, `_showcase/`)
   - 图片资源 (`assets/images/`)
   - SEO相关文件 (`sitemap.xml`, `robots.txt`)

2. **手动触发**: 您可以在GitHub Actions页面手动触发工作流

3. **定期检查**: 每周一上午8点UTC自动运行，确保搜索引擎了解最新内容

## 首次设置

### 1. 设置GitHub Secret

您需要在GitHub仓库中设置IndexNow API密钥：

1. 进入您的GitHub仓库
2. 点击 `Settings` > `Secrets and variables` > `Actions`
3. 点击 `New repository secret`
4. 名称: `INDEXNOW_API_KEY`
5. 值: `5a933d53056640af8bee125d8f287aa5`
6. 点击 `Add secret`

### 2. 验证API密钥文件

网站根目录下的 `5a933d53056640af8bee125d8f287aa5.txt` 文件包含您的API密钥，这是IndexNow验证网站所有权所必需的。

## 使用方法

### 自动通知

设置完成后，IndexNow通知将完全自动化。当您更新内容并推送到GitHub时，工作流将自动运行并向IndexNow发送通知。

### 手动触发

如果您想立即通知所有页面（而不仅仅是更改的页面）：

1. 进入GitHub仓库的 `Actions` 页面
2. 选择 `IndexNow 通知` 工作流
3. 点击 `Run workflow`
4. 勾选 `notify_all` 选项
5. 点击 `Run workflow`

### 查看结果

每次运行后，您可以：

1. 在Actions页面查看工作流日志
2. 下载 `indexnow-results` 工件查看详细结果
3. 检查网站根目录下的 `indexnow_result.json` 文件（仅在本地运行时）

## 故障排除

### 工作流未触发

检查以下事项：

1. 确认推送的文件类型符合触发条件
2. 确认推送到正确的分支（main或master）
3. 检查GitHub Actions是否在仓库中启用

### API调用失败

1. 验证 `INDEXNOW_API_KEY` Secret是否正确设置
2. 检查API密钥验证文件是否可访问
3. 查看工作流日志中的错误信息

### 部分URL提交失败

IndexNow API有速率限制。如果部分批次失败：

1. 检查是否有网络连接问题
2. 确认URL格式正确
3. 稍后重试（工作流已包含自动延迟）

## 高级配置

### 修改触发条件

编辑 `.github/workflows/indexnow.yml` 文件中的 `on` 部分来修改触发条件。

### 自定义通知范围

默认情况下，脚本会通知sitemap.xml中的所有URL。您可以修改 `.github/scripts/indexnow.py` 来：

1. 只通知特定类型的页面
2. 排除某些URL
3. 自定义批量大小

### 添加更多搜索引擎

IndexNow API会自动将您的URL提交给参与的搜索引擎（包括必应、雅虎等）。无需额外配置。

## 性能考虑

- 脚本支持批量提交，最多一次10,000个URL
- 自动添加延迟以避免API速率限制
- 只在内容实际更改时触发通知，避免不必要的API调用

## 安全注意事项

- API密钥存储在GitHub Secrets中，不会暴露在代码中
- API密钥验证文件是必需的，但仅包含密钥本身
- 工作流只具有读取权限，无法修改您的代码

## 更新和维护

### 更新API密钥

如果需要更换API密钥：

1. 在IndexNow网站获取新密钥
2. 更新GitHub Secret `INDEXNOW_API_KEY`
3. 更新网站根目录下的密钥验证文件名和内容

### 更新脚本

如果需要修改通知逻辑：

1. 编辑 `.github/scripts/indexnow.py`
2. 测试更改：可以手动触发工作流
3. 提交更改到仓库

## 相关资源

- [IndexNow官方网站](https://www.indexnow.org/)
- [IndexNow API文档](https://www.indexnow.org/documentation)
- [GitHub Actions文档](https://docs.github.com/en/actions)

## 支持

如果您遇到问题或需要帮助：

1. 查看GitHub Actions日志
2. 检查本文档的故障排除部分
3. 在仓库中创建Issue