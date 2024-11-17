---
title: "在 Netlify 上免费托管您的 Hugo 网站"
date: 2024-11-10
draft: false
tags: ["markdown", "tutorial", "hugo", "blog"]
image: "/img/posts/img-4.jpg"
Description: "This guide should help you get started with hosting your Hugo site on Netlify. Would you like me to explain any part in more detail?"
featured: true
---

# 在 Netlify 上免费托管您的 Hugo 网站

## 什么是 Netlify？
Netlify 是一个免费的网站托管服务 - 可以将其视为让所有人都能在互联网上访问您网站的平台。它特别适合静态网站（如使用 Hugo 构建的网站），因为：
- 基础使用完全免费
- 速度非常快
- 设置简单
- 当您进行更改时自动更新网站

## 在 Netlify 上设置您的网站

### 第一步：准备配置
在项目主文件夹中创建一个名为 `netlify.toml` 的文件。此文件告诉 Netlify 如何处理您的网站：

```toml
[build]
publish = "public"          # 告诉 Netlify 您的完成网站文件在哪里
command = "hugo --gc --minify"  # 告诉 Netlify 使用 Hugo 构建您的网站

# 主网站的设置
[context.production.environment]
HUGO_VERSION = "0.82.0"    # 指定使用的 Hugo 版本
HUGO_ENV = "production"    # 告诉 Hugo 这是用于您的正式网站
HUGO_ENABLEGITINFO = "true"  # 允许 Hugo 使用 Git 信息

# 不同部署场景的设置
[context.split1]
command = "hugo --gc --minify --enableGitInfo"

[context.split1.environment]
HUGO_VERSION = "0.82.0"
HUGO_ENV = "production"

# 预览部署的设置（当您想测试更改时）
[context.deploy-preview]
command = "hugo --gc --minify --buildFuture -b $DEPLOY_PRIME_URL"

[context.deploy-preview.environment]
HUGO_VERSION = "0.82.0"

# 分支部署的设置
[context.branch-deploy]
command = "hugo -b $DEPLOY_PRIME_URL"

[context.branch-deploy.environment]
HUGO_VERSION = "0.82.0"

[context.next.environment]
HUGO_ENABLEGITINFO = "true"
```

### 第二步：选择部署方式

您有两种方式将网站部署到 Netlify：

#### 方式一：直接上传
1. 在本地构建 Hugo 站点（运行 `hugo` 命令）
2. 访问 Netlify 网站
3. 注册或登录
4. 将 `public` 文件夹拖放到 Netlify 的仪表板
5. 您的网站就上线了！

#### 方式二：GitHub 集成（推荐）
1. 将您的 Hugo 站点放在 GitHub 上
2. 登录 Netlify
3. 点击"New site from Git"
4. 选择 GitHub 并选择您的仓库
5. Netlify 将自动：
   - 在您更新 GitHub 时构建您的网站
   - 部署您的更改
   - 处理所有技术细节

### 第三步：自定义域名（可选）
- Netlify 提供免费域名，如 `your-site-name.netlify.app`
- 您可以通过 Netlify 的设置添加自己的自定义域名
- Netlify 甚至提供免费的 HTTPS 证书

## 成功提示
- 在推送到 GitHub 之前始终在本地测试您的网站
- 确保 `netlify.toml` 中的 Hugo 版本与您本地使用的版本匹配
- 如果使用 GitHub，请将 `public` 文件夹放在 `.gitignore` 文件中
- 使用 Netlify 的部署预览来检查更改是否生效

## 常见问题及解决方案
1. **构建失败**
   - 检查您的 Hugo 版本是否与 netlify.toml 匹配
   - 确保包含所有主题文件
   
2. **图片不显示**
   - 检查图片路径是否正确
   - 确保图片在 static 文件夹中

3. **部署停滞**
   - 检查您的仓库权限
   - 验证 netlify.toml 中的构建设置

需要帮助？查看 Netlify 的文档或他们的社区论坛寻求支持！