#!/usr/bin/env python3
import requests
import json
import sys

# 飞书机器人配置（从 openclaw.json 读取的 default 账户）
APP_ID = "cli_a934dc3183389cb6"
APP_SECRET = "nRKMmPSH7QvqlyZlSmyl5guce5NQPBiZ"

def get_tenant_access_token():
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get("code") != 0:
        print(f"获取 token 失败: {result}")
        sys.exit(1)
    return result["tenant_access_token"]

def search_chat(token, query):
    """搜索群聊"""
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "user_id_type": "open_id",
        "query": query,
        "page_size": 20
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    if len(sys.argv) < 2:
        query = "News"
    else:
        query = sys.argv[1]
    
    print(f"正在搜索群聊: {query}")
    token = get_tenant_access_token()
    result = search_chat(token, query)
    
    print("\n搜索结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("code") == 0 and result.get("data"):
        items = result["data"].get("items", [])
        if items:
            print(f"\n找到 {len(items)} 个群聊:")
            for idx, chat in enumerate(items, 1):
                print(f"\n{idx}. 群名称: {chat.get('name')}")
                print(f"   群 ID: {chat.get('chat_id')}")
                print(f"   群描述: {chat.get('description')}")
                print(f"   成员数: {chat.get('member_count')}")
        else:
            print("\n未找到匹配的群聊")

if __name__ == "__main__":
    main()
