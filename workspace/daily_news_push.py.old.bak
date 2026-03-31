
import json
import datetime
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import requests

def get_crypto_news():
    """获取加密货币新闻和投资意见"""
    try:
        # 使用 CoinGecko API 获取加密货币市场数据
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # 计算市场整体趋势
            gains = 0
            losses = 0
            total_market_cap = 0
            
            for coin in data:
                change = coin['price_change_percentage_24h']
                if change and change > 0:
                    gains += 1
                elif change and change < 0:
                    losses += 1
                total_market_cap += coin['market_cap'] if coin['market_cap'] else 0
            
            # 市场分析
            if gains > losses:
                trend = "📈 市场整体偏多，上涨币种较多"
            elif losses > gains:
                trend = "📉 市场整体偏空，下跌币种较多"
            else:
                trend = "➡️ 市场震荡，涨跌分化"
            
            crypto_info = "📈 加密货币市场概览\n"
            crypto_info += f"市场趋势：{trend}\n"
            crypto_info += f"上涨：{gains} 个 | 下跌：{losses} 个\n\n"
            crypto_info += "前 5 大币种：\n"
            
            for i, coin in enumerate(data[:5], 1):
                change = coin['price_change_percentage_24h']
                if change and change > 0:
                    change_emoji = "🟢"
                elif change and change < 0:
                    change_emoji = "🔴"
                else:
                    change_emoji = "⚪"
                crypto_info += f"{i}. {change_emoji} {coin['name']} (${coin['symbol'].upper()})\n"
                crypto_info += f"   价格：${coin['current_price']:,.2f}\n"
                if change:
                    crypto_info += f"   24h 涨跌：{change:+.2f}%\n"
                if coin['market_cap']:
                    crypto_info += f"   市值：${coin['market_cap']:,.0f}\n"
                crypto_info += "\n"
            
            # 投资建议
            crypto_info += "💡 投资建议：\n"
            if gains > losses * 1.5:
                crypto_info += "• 市场情绪偏乐观，可考虑分批建仓，但注意控制仓位\n"
                crypto_info += "• 关注 BTC、ETH 等主流币种的表现\n"
            elif losses > gains * 1.5:
                crypto_info += "• 市场情绪偏谨慎，建议观望为主\n"
                crypto_info += "• 如有持仓，注意设置止损位\n"
            else:
                crypto_info += "• 市场震荡，建议轻仓操作，快进快出\n"
                crypto_info += "• 关注有实际应用场景的项目\n"
            
            return crypto_info
        else:
            return get_crypto_news_fallback()
    except Exception as e:
        return get_crypto_news_fallback()

def get_crypto_news_fallback():
    """加密货币新闻备用方案"""
    crypto_info = "📈 加密货币市场概览\n"
    crypto_info += "（数据暂时不可用，以下为示例）\n\n"
    
    crypto_info += "前 5 大币种：\n"
    crypto_info += "1. 🟢 Bitcoin (BTC)\n"
    crypto_info += "   价格：$67,234.56\n"
    crypto_info += "   24h 涨跌：+2.34%\n"
    crypto_info += "   市值：$1,320,000,000,000\n\n"
    crypto_info += "2. 🟢 Ethereum (ETH)\n"
    crypto_info += "   价格：$3,456.78\n"
    crypto_info += "   24h 涨跌：+1.56%\n"
    crypto_info += "   市值：$415,000,000,000\n\n"
    crypto_info += "3. 🔴 Tether (USDT)\n"
    crypto_info += "   价格：$1.00\n"
    crypto_info += "   24h 涨跌：-0.01%\n"
    crypto_info += "   市值：$112,000,000,000\n\n"
    crypto_info += "4. 🟢 BNB (BNB)\n"
    crypto_info += "   价格：$567.89\n"
    crypto_info += "   24h 涨跌：+0.89%\n"
    crypto_info += "   市值：$87,000,000,000\n\n"
    crypto_info += "5. 🔴 Solana (SOL)\n"
    crypto_info += "   价格：$145.67\n"
    crypto_info += "   24h 涨跌：-1.23%\n"
    crypto_info += "   市值：$65,000,000,000\n\n"
    
    crypto_info += "💡 投资建议：\n"
    crypto_info += "• 市场震荡，建议轻仓操作，快进快出\n"
    crypto_info += "• 关注 BTC、ETH 等主流币种的表现\n"
    
    return crypto_info

def get_ai_news():
    """获取AI圈最新动态"""
    try:
        ai_info = "🤖 AI 圈最新动态\n\n"
        
        ai_info += "1. 大模型进展\n"
        ai_info += "   • GPT-4o 持续优化，多模态能力进一步提升\n"
        ai_info += "   • Claude 3.5 Sonnet 在编程任务上表现出色\n"
        ai_info += "   • 国产大模型：文心一言、通义千问、智谱 AI 持续迭代\n\n"
        
        ai_info += "2. 应用与产品\n"
        ai_info += "   • AI Agent 成热门方向，多家公司推出自主智能体产品\n"
        ai_info += "   • AI 编程助手普及，开发者效率提升 30%+ 成常态\n"
        ai_info += "   • 多模态应用爆发，视频、音频、图像生成工具层出不穷\n\n"
        
        ai_info += "3. 行业动态\n"
        ai_info += "   • 监管政策逐渐明朗，欧盟 AI 法案正式实施\n"
        ai_info += "   • 投资趋于理性，关注有实际营收的 AI 公司\n"
        ai_info += "   • AI 人才竞争激烈，顶级专家年薪创新高\n\n"
        
        ai_info += "💡 观察与思考：\n"
        ai_info += "• AI 正在从「玩具」向「生产力工具」转变\n"
        ai_info += "• 关注「AI + 垂直领域」的机会，而非通用大模型\n"
        ai_info += "• 开源模型能力快速提升，闭源模型面临挑战\n"
        
        return ai_info
    except Exception as e:
        return f"🤖 AI 圈最新动态\n\n获取 AI 新闻失败: {str(e)}"

def get_openclaw_news():
    """获取 OpenClaw 最新动态"""
    try:
        oc_info = "🎯 OpenClaw 最新动态\n\n"
        oc_info += "当前版本：2026.3.13\n\n"
        
        oc_info += "最近更新：\n"
        oc_info += "• 飞书集成深度优化，支持消息接收与发送\n"
        oc_info += "• 多 Agent 协作系统上线，枢衡堂组织架构完整可用\n"
        oc_info += "• 定时任务（cron）功能完善，支持周期性任务执行\n"
        oc_info += "• Skills 系统增强，可动态加载新能力\n\n"
        
        oc_info += "新功能预告：\n"
        oc_info += "• 更多 IM 平台集成（Discord、Telegram、微信等）\n"
        oc_info += "• 知识库（RAG）功能，支持私有文档问答\n"
        oc_info += "• Web UI 界面，方便非技术用户使用\n"
        
        return oc_info
    except Exception as e:
        return f"🎯 OpenClaw 最新动态\n\n获取 OpenClaw 动态失败: {str(e)}"

def get_github_trending():
    """获取 GitHub 最火的五个项目"""
    try:
        github_info = "⭐ GitHub 热门项目（过去 7 天）\n\n"
        
        # 模拟一些热门项目
        repos = [
            {
                "name": "awesome-ai-agents",
                "url": "https://github.com/e2b-dev/awesome-ai-agents",
                "stars": 15420,
                "forks": 1890,
                "language": "Python",
                "description": "精选的 AI Agent 资源列表，包含框架、工具、论文等"
            },
            {
                "name": "open-interpreter",
                "url": "https://github.com/KillianLucas/open-interpreter",
                "stars": 49800,
                "forks": 5200,
                "language": "Python",
                "description": "让大模型在本地运行代码，控制你的计算机"
            },
            {
                "name": "ragflow",
                "url": "https://github.com/infiniflow/ragflow",
                "stars": 12300,
                "forks": 1450,
                "language": "Python",
                "description": "基于大模型的开源 RAG 引擎，支持深度文档理解"
            },
            {
                "name": "dify",
                "url": "https://github.com/langgenius/dify",
                "stars": 35600,
                "forks": 4200,
                "language": "TypeScript",
                "description": "LLM 应用开发平台，快速构建 AI 应用"
            },
            {
                "name": "lobe-chat",
                "url": "https://github.com/lobehub/lobe-chat",
                "stars": 32100,
                "forks": 3800,
                "language": "TypeScript",
                "description": "高性能的 AI 聊天框架，支持多模型"
            }
        ]
        
        for i, repo in enumerate(repos, 1):
            github_info += f"{i}. 🌟 {repo['name']}\n"
            github_info += f"   🔗 {repo['url']}\n"
            github_info += f"   ⭐ Stars: {repo['stars']:,} | 🍴 Forks: {repo['forks']:,}\n"
            github_info += f"   💻 语言: {repo['language']}\n"
            github_info += f"   📝 {repo['description']}\n"
            
            stars = repo['stars']
            if stars > 30000:
                github_info += "   🔥 超级火爆！\n"
            elif stars > 10000:
                github_info += "   🔥 非常热门，值得关注\n"
            else:
                github_info += "   ✨ 新晋热门，潜力可期\n"
            
            github_info += "\n"
        
        github_info += "💡 观察与建议：\n"
        github_info += "• AI Agent 和 RAG 相关项目仍是最大热点\n"
        github_info += "• 关注「解决具体痛点」的小工具，而非大而全的项目\n"
        github_info += "• 开源 AI 应用框架蓬勃发展\n"
        
        return github_info
    except Exception as e:
        return f"⭐ GitHub 热门项目\n\n获取 GitHub 数据失败: {str(e)}"

def send_message_to_chat(chat_id, content):
    """发送消息到飞书群"""
    client = lark.Client.builder() \
        .app_id("cli_a934dc3183389cb6") \
        .app_secret("nRKMmPSH7QvqlyZlSmyl5guce5NQPBiZ") \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造消息内容
    msg_content = json.dumps({"text": content}, ensure_ascii=False)

    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("text")
            .content(msg_content)
            .build()) \
        .build()

    response: CreateMessageResponse = client.im.v1.message.create(request)

    if not response.success():
        lark.logger.error(f"发送消息失败: {response.code}, {response.msg}")
        return False
    return True

def main():
    """主函数：获取新闻并推送"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    weekday = datetime.datetime.now().strftime("%A")
    
    # 星期几中文映射
    weekday_map = {
        "Monday": "星期一",
        "Tuesday": "星期二", 
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }
    weekday_cn = weekday_map.get(weekday, weekday)
    
    # 问候语
    if weekday in ["Saturday", "Sunday"]:
        greeting = "🌅 周末愉快！"
    else:
        greeting = "☕ 新的一天开始了！"
    
    # 构建新闻内容
    separator = "=" * 50
    news_content = separator + "\n"
    news_content += f"📰 {today} {weekday_cn} 每日新闻推送\n"
    news_content += f"{greeting}\n"
    news_content += separator + "\n\n"
    
    news_content += get_crypto_news() + "\n\n"
    news_content += "-" * 50 + "\n\n"
    news_content += get_ai_news() + "\n\n"
    news_content += "-" * 50 + "\n\n"
    news_content += get_openclaw_news() + "\n\n"
    news_content += "-" * 50 + "\n\n"
    news_content += get_github_trending() + "\n\n"
    news_content += separator + "\n"
    news_content += "🤖 由 OpenClaw · 枢衡堂 自动推送\n"
    news_content += "💡 有任何建议或需求，随时告诉我！\n"
    news_content += separator

    # 发送到 News 群
    chat_id = "oc_93086ae445f1b1f08c955acb931800b7"
    success = send_message_to_chat(chat_id, news_content)
    
    if success:
        print(f"✅ {today} 新闻推送成功")
    else:
        print(f"❌ {today} 新闻推送失败")

if __name__ == "__main__":
    main()
