
#!/usr/bin/env python3
"""
抖音视频分析工具 - MVP 版本
功能：
1. 解析抖音视频标题和描述
2. 提取视频中的网站链接
3. 识别可能的项目名称
"""

import sys
import re
import json
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
    keywords = ['项目', '平台', '协议', '代币', '币', '链', 'DAO', '基金会', '实验室', '科技', '网络']
    sentences = re.split(r'[。！？!?\n]', text)
    
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence:
                # 提取关键词前后的内容
                idx = sentence.find(keyword)
                start = max(0, idx - 15)
                end = min(len(sentence), idx + 10)
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
    
    return unique_projects[:10]  # 最多返回10个


def analyze_douyin_video(url):
    """
    分析抖音视频
    返回：包含视频信息的字典
    """
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # 不下载视频
            'skip_download': True,
        }
        
        result = {
            'success': False,
            'error': None,
            'title': None,
            'description': None,
            'uploader': None,
            'urls': [],
            'projects': [],
            'full_text': ''
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                result['success'] = True
                result['title'] = info.get('title', '')
                result['description'] = info.get('description', '')
                result['uploader'] = info.get('uploader', '')
                
                # 合并标题和描述用于分析
                full_text = f"{result['title']}\n{result['description']}"
                result['full_text'] = full_text
                
                # 提取链接
                result['urls'] = extract_urls(full_text)
                
                # 提取项目名称
                result['projects'] = extract_project_names(full_text)
                
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                if 'Private video' in error_msg:
                    result['error'] = '视频是私有的，无法访问'
                elif 'Video unavailable' in error_msg:
                    result['error'] = '视频不存在或已被删除'
                elif 'Sign in' in error_msg:
                    result['error'] = '需要登录才能访问'
                else:
                    result['error'] = f'无法解析视频: {error_msg[:100]}'
        
        return result
        
    except ImportError:
        return {
            'success': False,
            'error': '缺少 yt-dlp 库，请先安装: pip install yt-dlp'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'分析失败: {str(e)}'
        }


def print_analysis_result(result):
    """格式化输出分析结果"""
    print("=" * 60)
    print("📹 抖音视频分析结果")
    print("=" * 60)
    
    if not result['success']:
        print(f"❌ 错误: {result['error']}")
        print("=" * 60)
        return
    
    print(f"\n🎬 标题: {result['title'] or '无'}")
    print(f"👤 作者: {result['uploader'] or '未知'}")
    
    if result['description']:
        desc = result['description']
        if len(desc) > 200:
            desc = desc[:200] + "..."
        print(f"\n📝 描述: {desc}")
    
    if result['urls']:
        print(f"\n🔗 发现的链接 ({len(result['urls'])} 个):")
        for i, url in enumerate(result['urls'], 1):
            print(f"   {i}. {url}")
    
    if result['projects']:
        print(f"\n💡 可能的项目/关键词 ({len(result['projects'])} 个):")
        for i, project in enumerate(result['projects'], 1):
            print(f"   {i}. {project}")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python douyin_analyzer.py <抖音视频链接>")
        print("\n示例:")
        print("  python douyin_analyzer.py https://www.douyin.com/video/xxxxxx")
        return
    
    url = sys.argv[1]
    
    print(f"🔍 正在分析视频: {url}")
    print("请稍候...\n")
    
    result = analyze_douyin_video(url)
    print_analysis_result(result)


if __name__ == "__main__":
    main()
