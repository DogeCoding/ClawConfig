
#!/usr/bin/env python3
"""
视频文本分析工具 - MVP 版本
功能：
1. 从视频标题/描述中提取网站链接
2. 识别可能的项目名称
3. 总结核心内容

使用方法：
- 交互式: python video_text_analyzer.py
- 命令行: python video_text_analyzer.py "标题" "描述"
"""

import sys
import re
from urlextract import URLExtract

# 初始化链接提取器
extractor = URLExtract()


def extract_urls(text):
    """从文本中提取所有 URL"""
    if not text:
        return []
    
    urls = extractor.find_urls(text)
    
    # 清理和去重
    cleaned_urls = []
    seen = set()
    
    for url in urls:
        # 移除末尾的标点符号
        url = url.rstrip('.,;!?:））"\'')
        if url and url not in seen:
            seen.add(url)
            cleaned_urls.append(url)
    
    return cleaned_urls


def extract_project_names(text):
    """从文本中提取可能的项目名称"""
    if not text:
        return []
    
    project_names = []
    
    # 模式1: GitHub 项目 (用户名/项目名)
    github_pattern = r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)'
    github_matches = re.findall(github_pattern, text)
    project_names.extend([f"GitHub: {m}" for m in github_matches if '/' in m])
    
    # 模式2: @提及的项目/账号
    mention_pattern = r'@([a-zA-Z0-9_-]+)'
    mention_matches = re.findall(mention_pattern, text)
    project_names.extend([f"提及: @{m}" for m in mention_matches])
    
    # 模式3: 常见的项目标识词
    keywords = ['项目', '平台', '协议', '代币', '币', '链', 'DAO', '基金会', '实验室', '科技', '网络', 'AI', '大模型']
    sentences = re.split(r'[。！？!?\n]', text)
    
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence:
                # 提取关键词前后的内容
                idx = sentence.find(keyword)
                start = max(0, idx - 20)
                end = min(len(sentence), idx + 15)
                context = sentence[start:end].strip()
                if context and len(context) > 3:
                    project_names.append(f"候选: {context}")
    
    # 去重
    seen = set()
    unique_projects = []
    for p in project_names:
        if p not in seen:
            seen.add(p)
            unique_projects.append(p)
    
    return unique_projects[:15]  # 最多返回15个


def summarize_content(text):
    """简单的内容摘要"""
    if not text:
        return "无内容"
    
    # 提取第一句话
    first_sentence = re.split(r'[。！？!?\n]', text)[0].strip()
    
    # 统计关键词
    keywords = ['AI', '大模型', 'OpenAI', 'GPT', 'Claude', '项目', '发布', '更新']
    found_keywords = [k for k in keywords if k in text]
    
    summary = first_sentence[:100]
    if len(first_sentence) > 100:
        summary += "..."
    
    return summary


def analyze_text(title, description=""):
    """分析文本内容"""
    full_text = f"{title}\n{description}".strip()
    
    result = {
        'title': title,
        'description': description,
        'full_text': full_text,
        'urls': extract_urls(full_text),
        'projects': extract_project_names(full_text),
        'summary': summarize_content(full_text)
    }
    
    return result


def print_analysis_result(result):
    """格式化输出分析结果"""
    print("=" * 60)
    print("📝 视频文本分析结果")
    print("=" * 60)
    
    if result['title']:
        print(f"\n🎬 标题: {result['title']}")
    
    if result['description']:
        desc = result['description']
        if len(desc) > 300:
            desc = desc[:300] + "..."
        print(f"\n📝 描述: {desc}")
    
    print(f"\n💡 内容摘要: {result['summary']}")
    
    if result['urls']:
        print(f"\n🔗 发现的链接 ({len(result['urls'])} 个):")
        for i, url in enumerate(result['urls'], 1):
            print(f"   {i}. {url}")
    
    if result['projects']:
        print(f"\n🌟 可能的项目/关键词 ({len(result['projects'])} 个):")
        for i, project in enumerate(result['projects'], 1):
            print(f"   {i}. {project}")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("📝 视频文本分析工具 - 交互式模式")
    print("=" * 60)
    print("\n请粘贴视频的标题和描述（按回车继续，留空则跳过）：")
    
    title = input("\n🎬 视频标题: ").strip()
    print("\n📝 视频描述（可多行，输入 'END' 结束）:")
    
    description_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        description_lines.append(line)
    
    description = '\n'.join(description_lines).strip()
    
    if not title and not description:
        print("\n❌ 没有输入内容，退出")
        return
    
    result = analyze_text(title, description)
    print_analysis_result(result)


def main():
    """主函数"""
    if len(sys.argv) == 1:
        interactive_mode()
    elif len(sys.argv) == 2:
        title = sys.argv[1]
        result = analyze_text(title)
        print_analysis_result(result)
    elif len(sys.argv) >= 3:
        title = sys.argv[1]
        description = ' '.join(sys.argv[2:])
        result = analyze_text(title, description)
        print_analysis_result(result)


if __name__ == "__main__":
    main()
