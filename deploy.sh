#!/bin/bash
# simple-web-cicd 一键部署脚本（在 ECS 上执行）
# 用法:
#   1) CI 把 simple-web.tar.gz 和 docker-compose.prod.yml 上传到 /opt/simple-web/
#   2) 在服务器上执行:  bash deploy.sh
set -euo pipefail

APP_DIR="/opt/simple-web"
IMAGE_FILE="simple-web.tar.gz"
IMAGE_NAME="simple-web:latest"
COMPOSE_FILE="docker-compose.prod.yml"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

if [ ! -d "$APP_DIR" ]; then
    log "创建目录 $APP_DIR"
    mkdir -p "$APP_DIR"
fi

cd "$APP_DIR"

log "[1/5] 检查部署文件..."
if [ ! -f "$IMAGE_FILE" ]; then
    log "错误: 找不到 $IMAGE_FILE"
    exit 1
fi
if [ ! -f "$COMPOSE_FILE" ]; then
    log "错误: 找不到 $COMPOSE_FILE"
    exit 1
fi
log "  OK: 部署文件齐备"

log "[2/5] 解压并加载 Docker 镜像..."
gunzip -f "$IMAGE_FILE"
docker load -i simple-web.tar
rm -f simple-web.tar
log "  OK: 镜像 $IMAGE_NAME 已加载"

log "[3/5] 准备 docker-compose.yml..."
cp "$COMPOSE_FILE" docker-compose.yml
log "  OK"

log "[4/5] 停止旧容器并启动新容器..."
docker compose down --remove-orphans || true
docker compose up -d
log "  OK"

log "[5/5] 健康检查..."
sleep 3
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80 || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log "[OK] 部署成功! HTTP: $HTTP_CODE"
else
    log "[WARN] 返回 $HTTP_CODE，查看日志:"
    docker compose logs --tail=30
fi

echo ""
log "=== 运行状态 ==="
docker compose ps

echo ""
log "=== 最近 10 条日志 ==="
docker compose logs --tail=10
