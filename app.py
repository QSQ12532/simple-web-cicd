"""
极简 Flask Web 应用 — CI/CD 实验演示
"""
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD 实验 — Flask App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .card {
            background: #fff; border-radius: 16px; padding: 48px 40px;
            max-width: 500px; width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { color: #333; font-size: 28px; margin-bottom: 8px; }
        .version { color: #764ba2; font-size: 14px; font-weight: 600; margin-bottom: 24px; }
        .status { display: inline-block; background: #e8f5e9; color: #2e7d32;
                  padding: 6px 16px; border-radius: 20px; font-size: 14px; margin-bottom: 24px; }
        .info { background: #f5f5f5; border-radius: 8px; padding: 16px;
                text-align: left; font-size: 13px; color: #666; line-height: 1.8; }
        .info span { color: #333; font-weight: 600; }
        .student {
            margin-top: 24px; padding: 16px; border-radius: 8px;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            text-align: center;
        }
        .student .title { font-size: 13px; color: #8c5a3c; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px; }
        .student .name { font-size: 22px; color: #333; font-weight: 700; margin-bottom: 4px; }
        .student .sid { font-family: "Courier New", monospace; font-size: 18px; color: #555; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 CI/CD 部署成功！</h1>
        <p class="version">Flask App v2.0 | Python {{ python_version }}</p>
        <div class="status">✅ 服务运行正常</div>
        <div class="info">
            <p><span>容器 ID：</span>{{ hostname }}</p>
            <p><span>部署时间：</span>{{ deploy_time }}</p>
            <p><span>环境：</span>{{ environment }}</p>
        </div>
        <div class="student">
            <p class="title">软件工程导论 · 实验项目</p>
            <p class="name">植天然</p>
            <p class="sid">2440666146</p>
        </div>
    </div>
</body>
</html>"""


@app.route("/")
def index():
    import socket, platform, datetime
    return render_template_string(
        HTML,
        python_version=platform.python_version(),
        hostname=socket.gethostname(),
        deploy_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        environment="Production" if app.config.get("ENV") == "production" else "Development",
    )


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
