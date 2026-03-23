#!/usr/bin/env python3
import requests
import json
import sys
import uuid
import datetime
import os

# 飞书机器人配置
APP_ID = "cli_a934dc3183389cb6"
APP_SECRET = "nRKMmPSH7QvqlyZlSmyl5guce5NQPBiZ"
CHAT_ID = "oc_93086ae445f1b1f08c955acb931800b7"

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

def send_message(token, content):
    """发送消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "receive_id_type": "chat_id"
    }
    payload = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": content}, ensure_ascii=False),
        "uuid": str(uuid.uuid4())
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

def get_github_trending():
    """获取 GitHub 热榜（模拟）"""
    # 实际实现中调用 GitHub API
    return [
        {"name": "openclaw/openclaw", "desc": "OpenClaw - 下一代 AI 助手平台", "stars": "⭐ 12.5k"},
        {"name": "microsoft/ai-toolkit", "desc": "AI Toolkit for VS Code", "stars": "⭐ 8.3k"},
        {"name": "anthropic/cookbook", "desc": "Anthropic API 示例和教程", "stars": "⭐ 5.2k"},
        {"name": "huggingface/transformers", "desc": "🤗 Transformers: State-of-the-art Machine Learning", "stars": "⭐ 125k"},
        {"name": "langchain-ai/langchain", "desc": "🦜️🔗 LangChain - 构建 LLM 应用的框架", "stars": "⭐ 88k"}
    ]

def get_crypto_news():
    """获取加密货币动态（模拟）"""
    return [
        "BTC: $68,250 (+2.3%)",
        "ETH: $3,580 (+1.8%)",
        "SOL: $178 (+4.2%)",
        "市场分析: 比特币突破关键阻力位，看涨情绪上升"
    ]

def get_ai_news():
    """获取 AI 圈动态（模拟）"""
    return [
        "OpenAI 发布 GPT-5 预览版，多模态能力大幅提升",
        "Claude 3.5 Sonnet 上线，代码生成速度提升 2 倍",
        "谷歌 Gemini 2.0 开放 API，支持 1M token 上下文",
        "国内大模型混战：智谱、月之暗面、深度求索均有重大更新"
    ]

def get_openclaw_news():
    """获取 OpenClaw 动态（模拟）"""
    return [
        "OpenClaw 2026.3.13 已发布",
        "新增飞书群推送能力",
        "支持多 agent 协同工作流",
        "ClawHub 技能商店上线 50+ 新技能"
    ]

def get_general_news():
    """获取综合新闻（模拟）"""
    return [
        "科技：苹果发布 Vision Pro 2，售价降低 20%",
        "财经：美联储暗示可能降息，全球股市上涨",
        "体育：中国队在世界锦标赛中获得 3 金 2 银",
        "天气：全国大部分地区气温回升，注意增减衣物"
    ]

def build_message():
    """构建推送消息"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日 %A")
    
    message = f"🌅 早安 Graves！\n"
    message += f"📅 {today}\n\n"
    message += "=" * 30 + "\n\n"
    
    # 综合新闻
    message += "📰 今日要闻:\n"
    for news in get_general_news():
        message += f"  • {news}\n"
    message += "\n"
    
    # AI 动态
    message += "🤖 AI 圈动态:\n"
    for news in get_ai_news():
        message += f"  • {news}\n"
    message += "\n"
    
    # 加密货币
    message += "💰 加密货币:\n"
    for news in get_crypto_news():
        message += f"  • {news}\n"
    message += "\n"
    
    # OpenClaw 动态
    message += "🎯 OpenClaw 动态:\n"
    for news in get_openclaw_news():
        message += f"  • {news}\n"
    message += "\n"
    
    # GitHub 热榜
    message += "🔥 GitHub 热榜:\n"
    for idx, repo in enumerate(get_github_trending(), 1):
        message += f"  {idx}. {repo['name']} {repo['stars']}\n"
        message += f"      {repo['desc']}\n"
    
    message += "\n" + "=" * 30 + "\n"
    message += "祝你今天愉快！✨"
    
    return message

def main():
    print("正在生成早间新闻推送...")
    content = build_message()
    
    print("\n正在发送到飞书群...")
    token = get_tenant_access_token()
    result = send_message(token, content)
    
    if result.get("code") == 0:
        print("✅ 推送成功！")
    else:
        print(f"❌ 推送失败: {result.get('msg')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
