# 智能实验室预约系统

基于 **FastAPI + Vue 3 + AI Agent** 的全栈实验室预约管理平台，集成了角色权限、预约审核、文件管理、知识库问答及 LangGraph 智能 Agent 工作流。

## 技术栈

### 后端

| 类别    | 技术                                                 |
| ------- | ---------------------------------------------------- |
| 框架    | FastAPI                                              |
| ORM     | SQLAlchemy 2.0                                       |
| 数据库  | MySQL（通过 PyMySQL 连接）                           |
| 认证    | JWT（PyJWT）+ bcrypt 密码哈希                        |
| AI 引擎 | LangChain + LangGraph（Tool Calling + Agent 工作流） |
| 向量库  | ChromaDB（BAAI/bge-small-zh-v1.5 嵌入模型）          |
| LLM     | OpenAI 兼容接口（通义千问 DeepSeek 等）              |
| 运行    | Uvicorn                                              |

### 前端

| 类别          | 技术                              |
| ------------- | --------------------------------- |
| 框架          | Vue 3（Composition API）          |
| UI 组件库     | Element Plus                      |
| 路由          | Vue Router                        |
| HTTP 请求     | Axios（请求/响应拦截器）          |
| 流式交互      | fetch + SSE（Server-Sent Events） |
| Markdown 渲染 | marked + DOMPurify                |
| 构建工具      | Vite                              |
| 图标          | @element-plus/icons-vue           |

## 项目结构

```
lab-agent/
+-- backend/                       # 后端 FastAPI 项目
|   +-- app/
|   |   +-- main.py                # FastAPI 应用入口（CORS、异常处理、静态文件）
|   |   +-- config.py              # 配置类（数据库、JWT、LLM、上传限制）
|   |   +-- database.py            # SQLAlchemy 引擎、会话工厂、Base 模型
|   |   +-- api/                   # API 路由模块
|   |   |   +-- auth.py            # 登录 / 注册
|   |   |   +-- user.py            # 用户信息 CRUD
|   |   |   +-- lab.py             # 实验室 CRUD
|   |   |   +-- equipment.py       # 设备 CRUD
|   |   |   +-- reservation.py     # 预约创建/列表/取消/审核
|   |   |   +-- files.py           # 文件上传
|   |   |   +-- ai.py              # AI 对话（普通 + SSE 流式）
|   |   +-- models/                # SQLAlchemy 数据模型
|   |   |   +-- user.py            # User（学生/管理员）
|   |   |   +-- lab.py             # Lab
|   |   |   +-- equipment.py       # Equipment（关联 Lab）
|   |   |   +-- reservation.py     # Reservation（关联 User/Lab/Equipment）
|   |   +-- schemas/               # Pydantic 请求/响应模型
|   |   +-- services/              # 业务逻辑层
|   |   |   +-- auth_service.py    # 认证服务
|   |   |   +-- user_service.py    # 用户服务
|   |   |   +-- lab_service.py     # 实验室服务
|   |   |   +-- equipment_service.py # 设备服务
|   |   |   +-- reservation_service.py # 预约服务（含过期扫描）
|   |   |   +-- ai_service.py      # AI 对话服务
|   |   |   +-- agent_service.py   # LangGraph Agent 工作流
|   |   |   +-- agent_tools.py     # Agent 工具定义
|   |   |   +-- kb_service.py      # ChromaDB 知识库检索服务
|   |   +-- dependencies/auth.py   # 依赖注入
|   |   +-- common/                # 通用响应、异常处理
|   |   +-- utils/                 # 工具函数（JWT、密码）
|   +-- data/kb/                   # 知识库 Markdown 文档
|   +-- uploads/                   # 文件上传目录
|   +-- requirements.txt
+-- front-end/                     # 前端 Vue 3 项目
|   +-- src/
|   |   +-- App.vue                # 根组件
|   |   +-- router/index.js        # 路由配置（含导航守卫）
|   |   +-- layouts/Layout.vue     # 主布局（侧边栏菜单 + 顶栏）
|   |   +-- views/
|   |   |   +-- Login.vue          # 登录页
|   |   |   +-- Register.vue       # 注册页
|   |   |   +-- Home.vue           # 首页仪表盘
|   |   |   +-- LabList.vue        # 实验室列表（卡片布局）
|   |   |   +-- LabEquipment.vue   # 实验室设备详情
|   |   |   +-- Lab.vue            # 实验室管理（管理员）
|   |   |   +-- Equipment.vue      # 设备管理（管理员）
|   |   |   +-- User.vue           # 用户管理（管理员）
|   |   |   +-- MyReservation.vue  # 我的预约记录
|   |   |   +-- AuditReservation.vue # 预约审核（管理员）
|   |   |   +-- AIChat.vue         # AI 智能助手对话
|   |   |   +-- Profile.vue        # 个人信息
|   |   |   +-- Password.vue       # 修改密码
|   |   +-- api/                   # API 接口封装
|   |   +-- stores/                # Pinia 状态管理
|   |   +-- utils/                 # 工具函数
|   |   +-- assets/                # 静态资源
|   +-- vite.config.js             # Vite 配置（代理 API）
|   +-- package.json
+-- .env                           # 后端环境变量
+-- README.md
```

## 功能特性

### 角色与权限

- **学生（student）**：查看实验室列表、预约实验室/设备、查看我的预约、AI 智能助手
- **管理员（admin）**：实验室 CRUD、设备 CRUD、用户管理、预约审核、AI 智能助手

### 核心功能

1. **用户认证** — JWT 登录/注册，密码 bcrypt 加密，12 小时 token 有效期
2. **实验室管理** — 管理员维护实验室信息（名称、位置、容量、开放时间、封面、状态）
3. **设备管理** — 设备关联实验室（名称、型号规格、数量、状态、图片）
4. **预约流程** — 学生选择实验室/设备 -> 提交预约 -> 管理员审核 -> 通过/拒绝
5. **过期扫描** — 启动时自动创建异步任务，扫描并关闭过期预约
6. **文件上传** — 支持图片、文档、压缩包等类型，大小限制 100MB
7. **AI 智能助手** — RAG 知识库问答 + Agent 工具调用，支持 SSE 流式输出

### AI Agent 能力

基于 LangGraph 构建的智能 Agent，集成了以下工具：

| 工具                   | 功能                                                   |
| ---------------------- | ------------------------------------------------------ |
| search_lab_docs        | 检索 ChromaDB 知识库（预约规则、开放时间、安全规范等） |
| list_open_labs         | 查询当前开放的实验室列表                               |
| list_lab_equipments    | 查询指定实验室的设备信息                               |
| create_lab_reservation | 经用户确认后创建预约单                                 |
| get_today              | 获取服务器当前日期，用于日期推算                       |

Agent 工作流特点：

- 流式 SSE 推送：前端实时展示思考、检索等过程状态
- 工具调用过程可见：用户可以看到 Agent 每一步的执行状态
- 确认后再执行：预约提交前会向用户复述预约信息，获得确认后才落库
- System Prompt 严格约束：禁止 Agent 编造数据、提问日期时先调用 get_today

## 快速启动

### 环境要求

- Python >= 3.10
- Node.js >= 22.18
- MySQL 服务

### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt

# 3. 配置 .env 文件，确保 DATABASE_URL 指向 MySQL，配置 LLM 相关变量

# 4. 启动后端服务（自动建表 + 预热向量库）
uvicorn app.main:app --reload --port 8000
```

### 知识库初始化

将 Markdown 文档放入 backend/data/kb/ 目录，服务启动时 ChromaDB 自动建库。内置文档：

- 预约规则.md - 预约规则说明
- 开放时间.md - 开放时间安排
- 安全规范.md - 安全管理制度
- 设备使用.md - 设备使用注意事项

### 前端启动

```bash
cd front-end
npm install
npm run dev
```

Vite 已配置代理，/api 和 /uploads 自动代理到 http://127.0.0.1:8000。

## API 概览

所有 API 路径前缀为 /api，需携带 Authorization: Bearer token。

### 认证

| 方法 | 路径               | 说明 |
| ---- | ------------------ | ---- |
| POST | /api/auth/login    | 登录 |
| POST | /api/auth/register | 注册 |

### 用户

| 方法   | 路径               | 说明             | 权限     |
| ------ | ------------------ | ---------------- | -------- |
| GET    | /api/user/me       | 获取当前用户信息 | 登录用户 |
| PUT    | /api/user/me       | 更新个人信息     | 登录用户 |
| PUT    | /api/user/password | 修改密码         | 登录用户 |
| GET    | /api/user/list     | 用户列表分页     | 管理员   |
| POST   | /api/user          | 新增用户         | 管理员   |
| PUT    | /api/user/{id}     | 编辑用户         | 管理员   |
| DELETE | /api/user/{id}     | 删除用户         | 管理员   |

### 实验室

| 方法   | 路径          | 说明           | 权限     |
| ------ | ------------- | -------------- | -------- |
| GET    | /api/lab/list | 实验室分页列表 | 登录用户 |
| GET    | /api/lab/{id} | 实验室详情     | 登录用户 |
| POST   | /api/lab      | 新增实验室     | 管理员   |
| PUT    | /api/lab/{id} | 编辑实验室     | 管理员   |
| DELETE | /api/lab/{id} | 删除实验室     | 管理员   |

### 设备

| 方法   | 路径                | 说明         | 权限     |
| ------ | ------------------- | ------------ | -------- |
| GET    | /api/equipment/list | 设备分页列表 | 登录用户 |
| POST   | /api/equipment      | 新增设备     | 管理员   |
| PUT    | /api/equipment/{id} | 编辑设备     | 管理员   |
| DELETE | /api/equipment/{id} | 删除设备     | 管理员   |

### 预约

| 方法 | 路径                         | 说明         | 权限     |
| ---- | ---------------------------- | ------------ | -------- |
| POST | /api/reservation             | 创建预约     | 登录用户 |
| GET  | /api/reservation/list        | 预约分页列表 | 登录用户 |
| PUT  | /api/reservation/{id}/cancel | 取消预约     | 本人     |
| PUT  | /api/reservation/{id}/audit  | 审核预约     | 管理员   |

### AI

| 方法 | 路径                | 说明                 | 权限     |
| ---- | ------------------- | -------------------- | -------- |
| POST | /api/ai/chat        | AI 对话（普通 JSON） | 登录用户 |
| POST | /api/ai/chat/stream | AI 对话（SSE 流式）  | 登录用户 |

### 文件

| 方法 | 路径              | 说明     |
| ---- | ----------------- | -------- |
| POST | /api/files/upload | 文件上传 |

## 数据模型

### User（用户表）

| 字段     | 类型        | 说明                 |
| -------- | ----------- | -------------------- |
| id       | int (PK)    | 主键                 |
| username | string(50)  | 账号                 |
| password | string(255) | 密码（bcrypt 哈希）  |
| name     | string(50)  | 姓名                 |
| role     | string(50)  | 角色：student/admin  |
| email    | string(50)  | 邮箱                 |
| phone    | string(50)  | 手机号               |
| avatar   | string      | 头像 URL             |
| status   | int         | 状态：0-禁用，1-正常 |

### Lab（实验室表）

| 字段        | 类型        | 说明                 |
| ----------- | ----------- | -------------------- |
| id          | int (PK)    | 主键                 |
| name        | string(50)  | 实验室名称           |
| location    | string(100) | 位置                 |
| capacity    | int         | 容纳人数             |
| open_time   | string(20)  | 开放开始时间         |
| close_time  | string(20)  | 开放结束时间         |
| description | string(500) | 简介                 |
| img         | string(200) | 封面图 URL           |
| status      | int         | 状态：0-关闭，1-开放 |

### Equipment（设备表）

| 字段        | 类型        | 说明                 |
| ----------- | ----------- | -------------------- |
| id          | int (PK)    | 主键                 |
| lab_id      | int (FK)    | 所属实验室           |
| name        | string(50)  | 设备名称             |
| description | string(500) | 说明                 |
| img         | string(200) | 图片 URL             |
| spec        | string(100) | 型号规格             |
| quantity    | int         | 数量                 |
| status      | int         | 状态：0-维修，1-正常 |

### Reservation（预约表）

| 字段         | 类型        | 说明                                   |
| ------------ | ----------- | -------------------------------------- |
| id           | int (PK)    | 主键                                   |
| user_id      | int (FK)    | 预约人                                 |
| lab_id       | int (FK)    | 实验室                                 |
| equipment_id | int (FK)    | 设备（空表示预约实验室）               |
| date         | string(20)  | 预约日期                               |
| start_time   | string(20)  | 开始时间                               |
| end_time     | string(20)  | 结束时间                               |
| remark       | string(255) | 备注                                   |
| status       | int         | 0-待审核，1-已通过，2-已拒绝，3-已取消 |

## 环境变量

### 后端 .env

| 变量             | 说明                     |
| ---------------- | ------------------------ |
| DATABASE_URL     | MySQL 连接字符串         |
| JWT_SECRET_KEY   | JWT 签名密钥             |
| JWT_ALGORITHM    | JWT 算法（默认 HS256）   |
| JWT_EXPIRE_HOURS | Token 有效期（默认 12h） |
| LLM_API_KEY      | 大模型 API Key           |
| LLM_BASE_URL     | 大模型 API 地址          |
| LLM_MODEL        | 模型名称                 |

### 前端 .env.development

| 变量              | 说明              |
| ----------------- | ----------------- |
| VITE_API_BASE_URL | 后端 API 基础 URL |

## 开发说明

- 后端采用 Service 层模式，API 路由只处理请求解析和响应，业务逻辑集中在 services/ 层
- Agent 工作流使用 LangGraph 的 StateGraph，通过 astream_events 向前端推送 SSE 事件
- 向量库预热的 embedding 模型加载放在 lifespan 启动阶段，避免首个请求超时
- 预约过期扫描通过 asyncio.create_task 创建后台异步任务
- 前端用 fetch 原生 API 消费 SSE 流，Axios 用于普通 JSON 请求
- Markdown 渲染结果经过 DOMPurify 过滤，防止 XSS 攻击
