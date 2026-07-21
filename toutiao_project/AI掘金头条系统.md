# AI 掘金头条系统

AI 掘金头条系统是一个基于 **FastAPI + Vue3** 的智能新闻头条平台。该系统结合后端 API 和现代化前端，为用户提供新闻浏览、收藏管理、AI 推荐等功能，实现个性化的新闻阅读体验。

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260721180606403.png)



## 📂 项目结构

### 后端项目 (`toutiao_backend`)

```
toutiao_backend/
├── main.py                          # FastAPI 应用主入口
├── requirements.txt                 # Python 依赖清单
├── cache/                           # 缓存模块
│   ├── favorite_cache.py           # 收藏缓存
│   ├── news_cache.py               # 新闻缓存
│   └── users_cache.py              # 用户缓存
├── config/                          # 配置文件目录
│   ├── cache_conf.py               # Redis 缓存配置
│   └── db_conf.py                  # MySQL 数据库配置
├── crud/                            # 数据库操作层
│   ├── favorite.py                 # 收藏操作
│   ├── history.py                  # 历史记录操作
│   ├── news.py                     # 新闻操作
│   └── users.py                    # 用户操作
├── models/                          # 数据模型定义
│   ├── base.py                     # 基础模型
│   ├── category.py                 # 分类模型
│   ├── favorite.py                 # 收藏模型
│   ├── history.py                  # 历史模型
│   ├── news.py                     # 新闻模型
│   ├── user_token.py               # Token 模型
│   └── users.py                    # 用户模型
├── routers/                         # API 路由定义
│   ├── favorite.py                 # 收藏 API 端点
│   ├── history.py                  # 历史 API 端点
│   ├── news.py                     # 新闻 API 端点
│   └── users.py                    # 用户 API 端点
├── schemas/                         # 请求/响应数据结构
│   ├── base.py
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
└── utils/                           # 工具函数库
    ├── auth.py                     # 认证工具
    ├── db_transaction.py           # 数据库事务管理
    ├── exception_handlers.py       # 异常处理
    ├── exception.py                # 自定义异常
    ├── jwt.py                      # JWT 处理
    ├── response.py                 # 响应格式处理
    └── security.py                 # 安全相关函数
```



### 前端项目 (`xwzx-news`)

```
xwzx-news/
├── index.html                      # HTML 入口文件
├── package.json                    # 项目依赖配置
├── vite.config.js                  # Vite 构建配置
├── public/                         # 静态资源目录
└── src/
    ├── App.vue                    # 根组件
    ├── main.js                    # 应用入口
    ├── style.css                  # 全局样式
    ├── assets/                    # 静态资源
    ├── components/                # 可复用组件库
    │   ├── HelloWorld.vue
    │   ├── NewsItem.vue
    │   └── TabBar.vue
    ├── config/
    │   └── api.js                 # API 配置
    ├── i18n/                      # 国际化
    │   ├── index.js
    │   └── locales/
    │       ├── en-US.js
    │       └── zh-CN.js
    ├── router/
    │   └── index.js               # 路由配置
    ├── store/                     # 状态管理
    │   ├── index.js
    │   ├── language.js
    │   ├── theme.js
    │   ├── user.js
    │   └── modules/
    │       ├── favorite.js
    │       ├── history.js
    │       └── news.js
    └── views/                     # 页面组件
        ├── AIChat.vue             # AI 聊天页面
        ├── Category.vue           # 分类页面
        ├── Favorite.vue           # 收藏页面
        ├── History.vue            # 历史页面
        ├── Home.vue               # 首页
        ├── Login.vue              # 登录页面
        ├── My.vue                 # 我的页面
        ├── NewsDetail.vue         # 新闻详情页面
        ├── Profile.vue            # 个人资料页面
        ├── Register.vue           # 注册页面
        └── Settings.vue           # 设置页面
```



------

## 🛠 技术栈

### 后端技术栈

| 技术           | 版本    | 用途       |
| -------------- | ------- | ---------- |
| **FastAPI**    | 0.104.1 | Web 框架   |
| **Python**     | 3.8+    | 编程语言   |
| **MySQL**      | 8.0+    | 关系数据库 |
| **Redis**      | 4.0+    | 缓存数据库 |
| **SQLAlchemy** | 2.0+    | ORM 框架   |
| **Pydantic**   | 2.0+    | 数据验证   |
| **JWT**        | 最新    | 用户认证   |

### 前端技术栈

| 技术           | 版本   | 用途        |
| -------------- | ------ | ----------- |
| **Vue**        | 3.x    | 前端框架    |
| **Vite**       | 7.1.6  | 构建工具    |
| **Vant**       | 4.9.21 | UI 组件库   |
| **Vue Router** | 4.5.1  | 路由管理    |
| **Pinia**      | 3.0.3  | 状态管理    |
| **Axios**      | 1.12.2 | HTTP 客户端 |
| **Vue I18n**   | 9.8.0  | 国际化      |