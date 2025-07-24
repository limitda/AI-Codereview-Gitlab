# AI代码审查平台 - Vue3前端

这是一个基于 Vue3 + TypeScript + Element Plus 的前端应用，实现了与原始 `ui.py` Streamlit 应用相同的功能。

## 功能特性

- 🔐 **用户认证系统**：登录/登出，支持记住密码
- 📊 **数据展示**：合并请求(MR)和代码推送(Push)的审查日志
- 🔍 **数据筛选**：按日期范围、开发者、项目名称筛选
- 📈 **统计图表**：项目提交统计、项目平均得分、开发者提交统计、开发者平均得分、代码变更行数
- 📋 **详情查看**：查看 commit 详情的模态框
- 📱 **响应式设计**：适配不同屏幕尺寸

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript
- **Element Plus** - Vue 3 组件库
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理
- **ECharts** - 数据可视化图表库
- **Axios** - HTTP 客户端
- **Vite** - 现代化构建工具

## 项目结构

```
vue-frontend/
├── src/
│   ├── api/                 # API 接口
│   │   └── index.ts
│   ├── components/          # 组件
│   │   ├── Charts.vue       # 图表组件
│   │   ├── CommitModal.vue  # Commit详情模态框
│   │   └── DataTable.vue    # 数据表格组件
│   ├── router/              # 路由配置
│   │   └── index.ts
│   ├── stores/              # 状态管理
│   │   └── auth.ts          # 认证状态
│   ├── types/               # TypeScript 类型定义
│   │   └── index.ts
│   ├── utils/               # 工具函数
│   │   └── auth.ts          # 认证工具
│   ├── views/               # 页面组件
│   │   ├── Dashboard.vue    # 主仪表板
│   │   └── Login.vue        # 登录页面
│   ├── App.vue              # 根组件
│   └── main.ts              # 应用入口
├── index.html               # HTML 模板
├── package.json             # 项目依赖
├── tsconfig.json            # TypeScript 配置
├── vite.config.ts           # Vite 配置
└── README.md                # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
cd vue-frontend
npm install
```

### 2. 开发模式运行

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动。

### 3. 构建生产版本

```bash
npm run build
```

构建产物将生成在 `dist/` 目录。

### 4. 预览生产版本

```bash
npm run preview
```

## 配置说明

### 代理配置

在 `vite.config.ts` 中配置了 API 代理，将 `/api` 路径的请求代理到后端服务器：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5001',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

### 认证配置

在 `src/stores/auth.ts` 中配置用户凭据：

```typescript
const USER_CREDENTIALS = {
  admin: 'admin' // 默认用户名和密码
}
```

## API 接口

目前使用模拟数据，实际部署时需要后端提供以下 REST API 接口：

- `GET /api/mr-logs` - 获取合并请求日志
- `GET /api/push-logs` - 获取推送日志
- `GET /api/projects` - 获取项目列表
- `GET /api/authors` - 获取开发者列表

## 与原始 ui.py 的对应关系

| 原始功能 | Vue3 实现 |
|---------|-----------|
| Streamlit 登录页面 | `src/views/Login.vue` |
| Streamlit 主页面 | `src/views/Dashboard.vue` |
| 数据表格展示 | `src/components/DataTable.vue` |
| 统计图表 | `src/components/Charts.vue` |
| Commit详情模态框 | `src/components/CommitModal.vue` |
| 用户认证 | `src/stores/auth.ts` + `src/utils/auth.ts` |
| 数据获取 | `src/api/index.ts` |

## 部署建议

1. **开发环境**：使用 `npm run dev` 启动开发服务器
2. **生产环境**：
   - 运行 `npm run build` 构建项目
   - 将 `dist/` 目录部署到 Web 服务器（如 Nginx）
   - 配置反向代理将 API 请求转发到后端服务

## 注意事项

1. 当前使用模拟数据，需要后端提供相应的 REST API 接口
2. 认证机制与原始 Python 版本保持一致，使用 HMAC-SHA256 签名
3. 图表库使用 ECharts，提供丰富的交互功能
4. 响应式设计适配移动端和桌面端

## 开发说明

- 使用 TypeScript 提供类型安全
- 使用 Element Plus 组件库保证 UI 一致性
- 使用 Pinia 进行状态管理
- 使用 Vue Router 进行路由管理
- 使用 Vite 提供快速的开发体验
