# simple-web-cicd

软件工程导论课程考查项目 —— 基于 CI/CD 全流程的 Web 应用交付实战。

## 📁 项目结构

```
simple-web-cicd/
├── app.py                  # Flask Web 应用（主程序）
├── test_app.py             # 单元测试（pytest）
├── requirements.txt        # Python 依赖
├── Dockerfile              # 镜像构建脚本
├── .dockerignore           # Docker 构建忽略
├── .gitignore              # Git 忽略
├── docker-compose.yml      # 本地开发 compose
├── docker-compose.prod.yml # 生产环境 compose
├── deploy.sh               # ECS 一键部署脚本
└── .github/workflows/
    └── ci.yml              # GitHub Actions CI/CD 流水线
```

## 🚀 快速开始

### 1. 本地运行（开发环境）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 打开浏览器访问: http://127.0.0.1:8080
```

### 2. 运行测试

```bash
python -m pytest test_app.py -v
```

预期输出：3 个测试全部通过。

### 3. Docker 构建 & 运行

```bash
# 构建镜像
docker build -t simple-web:latest .

# 直接运行容器
docker run -d -p 8080:8080 --name simple-web simple-web:latest

# 或使用 docker-compose
docker compose up -d
```

## 🔧 CI/CD 流水线架构

GitHub Actions 工作流 `.github/workflows/ci.yml` 包含 4 个 Job：

| Job | 说明 | 触发时机 |
|-----|------|---------|
| ① validate | 安装 Python 依赖，执行 pytest 单元测试 | push / PR / manual |
| ② build | 构建 Docker 镜像，导出为 tar.gz artifact | push 到 main / manual |
| ③ deploy | 通过 SCP 上传镜像到 ECS，SSH 执行加载 + 启动 + 健康检查 | push 到 main |
| ④ notify | 汇总并输出各阶段结果（成功/失败） | 始终执行 |

**核心设计亮点**：镜像在 GitHub Actions runner 上构建，然后以 tar.gz 形式传输到 ECS，彻底绕过国内 ECS 拉取 Docker Hub 镜像的网络问题。

## ☁️ ECS 部署准备

### 1. 服务器要求

- 操作系统：Ubuntu 20.04+ / CentOS 7+
- 已安装 Docker 和 Docker Compose v2
- 开放 80 端口（安全组 + 防火墙）
- 创建部署目录：`mkdir -p /opt/simple-web`

### 2. GitHub Secrets 配置

在仓库 `Settings → Secrets and variables → Actions` 中添加：

| Secret | 说明 |
|--------|------|
| `SSH_HOST` | ECS 公网 IP 地址 |
| `SSH_USERNAME` | SSH 登录用户名（如 root） |
| `SSH_PRIVATE_KEY` | SSH 私钥内容（需在 ECS 上配置对应公钥到 `~/.ssh/authorized_keys`） |

### 3. SSH 密钥生成

```bash
# 在本地生成密钥对
ssh-keygen -t rsa -b 4096 -C "ci-cd@example.com"

# 将公钥添加到 ECS
ssh-copy-id -i ~/.ssh/id_rsa.pub root@<ECS_IP>

# 复制私钥内容到 GitHub Secrets
cat ~/.ssh/id_rsa
```

## 🎯 手动触发部署

1. 推送到 `main` 分支自动触发
2. 或访问 `Actions → Flask CI/CD → Run workflow` 手动触发
3. 等待流水线完成后访问 `http://<ECS_IP>`

## 🐛 常见问题排查

| 问题 | 解决方法 |
|------|---------|
| SSH 连接失败 | 检查安全组 22 端口、私钥格式、authorized_keys 权限（600） |
| 容器启动后访问 502 | `docker compose logs` 查看 Flask 日志，检查端口映射 |
| 健康检查失败 | ECS 上 `curl http://localhost:80` 排查，确认容器内 8080 → 主机 80 |
| GitHub Actions 失败 | 查看详细日志，检查 Secrets 是否配置、镜像 artifact 是否生成 |

## 📚 技术栈

- **语言**：Python 3.12
- **Web 框架**：Flask 3.1
- **测试**：pytest 8.3
- **容器化**：Docker + Docker Compose
- **CI/CD**：GitHub Actions
- **部署目标**：阿里云 / 腾讯云 / 华为云 ECS

## 📝 实验报告要点

1. **CI/CD 概念**：持续集成（CI）把代码变更自动编译测试；持续部署（CD）自动发布到生产
2. **Git 工作流**：feature → develop → main，PR 触发自动测试
3. **Docker 原理**：镜像（Image）= 只读模板，容器（Container）= 运行实例，分层存储 + Union FS
4. **架构设计**：验证 → 构建 → 部署，三段式流水线，故障隔离，失败即停

---

**License**: MIT
