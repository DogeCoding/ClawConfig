import json
import requests

# 飞书应用凭证
APP_ID = "cli_a934dc3183389cb6"
APP_SECRET = "nRKMmPSH7QvqlyZlSmyl5guce5NQPBiZ"
# 项目群ID
CHAT_ID = "oc_93086ae445f1b1f08c955acb931800b7"

def get_tenant_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            return data.get("tenant_access_token")
    print(f"获取tenant_access_token失败: {response.text}")
    return None

def send_project_list(token):
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # 构造消息内容
    content = {
        "text": """📋 【项目清单同步通知】（更新于2026-03-26）
当前Workspace下已有的项目：
1. 🎥 douyin-video-analyzer：抖音视频分析与数据采集工具
2. 🎬 film-projects：影视项目库（含《零下一百度生存日记》漫剧项目）
3. 📰 morning-news：早间新闻自动生成与推送工具
4. 🛠️ openclaw-media-production-skills：OpenClaw媒资生产技能集合
5. 📤 agent-outputs：AI生成内容统一输出目录

群公告权限配置中，本次先以消息形式同步~
        """
    }
    payload = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps(content)
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            print("项目清单已成功发送到飞书项目群！")
            return True
    print(f"发送消息失败: {response.text}")
    return False

def main():
    token = get_tenant_token()
    if not token:
        return False
    return send_project_list(token)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


