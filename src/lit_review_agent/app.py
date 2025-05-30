"""Streamlit web interface for Literature Review Agent."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

import streamlit as st

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from lit_review_agent.agent import LiteratureAgent
from lit_review_agent.utils.config import Config


def inject_custom_css():
    """注入2024年现代极简设计CSS样式。"""
    st.markdown("""
    <style>
    /* 现代字体导入 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* 2024现代设计变量 */
    :root {
        --primary: #000000;
        --secondary: #6b7280;
        --accent: #3b82f6;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;

        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --bg-hover: #f1f5f9;

        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;

        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --border-dark: #cbd5e1;

        --radius: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;

        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);

        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* 全局样式重置 */
    * {
        box-sizing: border-box;
    }

    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
        font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {display: none;}

    /* 现代化头部设计 */
    .modern-header {
        background: var(--bg-primary);
        padding: 4rem 0 3rem 0;
        text-align: center;
        border-bottom: 1px solid var(--border-light);
        margin-bottom: 2rem;
    }

    .modern-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        letter-spacing: -0.025em;
        line-height: 1.1;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .modern-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin: 0 0 0.5rem 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .modern-description {
        font-size: 0.875rem;
        color: var(--text-muted);
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* 现代卡片设计 */
    .modern-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .modern-card:hover {
        border-color: var(--border-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }

    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0;
        transition: var(--transition);
    }

    .modern-card:hover::before {
        opacity: 1;
    }

    /* 搜索区域 */
    .search-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        position: relative;
    }

    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--success), var(--accent));
        border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    }

    /* 现代输入框 */
    .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-sm) !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1) !important;
        background: var(--bg-primary) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }

    /* 现代按钮设计 */
    .stButton > button {
        background: var(--text-primary) !important;
        border: 1px solid var(--text-primary) !important;
        border-radius: var(--radius) !important;
        color: white !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-sm) !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        min-height: 2.75rem !important;
        line-height: 1.25 !important;
    }

    .stButton > button:hover {
        background: var(--text-secondary) !important;
        border-color: var(--text-secondary) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* 侧边栏现代化 */
    .css-1d391kg {
        background: var(--bg-primary) !important;
        border-right: 1px solid var(--border) !important;
        box-shadow: none !important;
    }

    .sidebar-modern {
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 0 0 1.5rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }

    .sidebar-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        letter-spacing: -0.025em;
    }

    /* 表单控件现代化 */
    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-sm) !important;
        transition: var(--transition) !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--border-dark) !important;
    }

    .stMultiSelect > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stSlider > div > div > div {
        background: var(--accent) !important;
        border-radius: 4px !important;
    }

    .stNumberInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        transition: var(--transition) !important;
    }

    .stNumberInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1) !important;
    }

    /* 现代指标卡片 */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .metric-card-modern {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .metric-card-modern:hover {
        border-color: var(--border-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .metric-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent);
        opacity: 0;
        transition: var(--transition);
    }

    .metric-card-modern:hover::before {
        opacity: 1;
    }

    .metric-value-modern {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
        line-height: 1;
        letter-spacing: -0.025em;
    }

    .metric-label-modern {
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }

    /* 现代论文卡片 */
    .paper-card-modern {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .paper-card-modern:hover {
        border-color: var(--border-dark);
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }

    /* 确保卡片内的Streamlit组件样式正确 */
    .paper-card-modern .stMarkdown {
        margin-bottom: 0.75rem;
    }

    .paper-card-modern .stMarkdown:last-child {
        margin-bottom: 0;
    }

    .paper-card-modern p {
        margin-bottom: 0.5rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
    }

    .paper-card-modern strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    .paper-number-modern {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: var(--bg-secondary);
        color: var(--text-secondary);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
        border: 1px solid var(--border);
    }

    .paper-title-modern {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 2.5rem 1rem 0;
        line-height: 1.4;
        letter-spacing: -0.025em;
    }

    .paper-meta-modern {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1rem;
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 500;
    }

    .paper-meta-item-modern {
        display: flex;
        align-items: center;
        gap: 0.375rem;
        background: var(--bg-secondary);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        border: 1px solid var(--border);
    }

    .paper-abstract-modern {
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 1rem 0;
        font-size: 0.875rem;
    }

    .paper-keywords-modern {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }

    .keyword-tag-modern {
        background: var(--bg-secondary);
        color: var(--text-secondary);
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid var(--border);
        transition: var(--transition);
    }

    .keyword-tag-modern:hover {
        background: var(--accent);
        color: white;
        border-color: var(--accent);
        transform: scale(1.05);
    }

    .paper-actions-modern {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .paper-link-modern {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.5rem 1rem;
        border-radius: var(--radius);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.75rem;
        transition: var(--transition);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        background: var(--bg-secondary);
    }

    .paper-link-modern:hover {
        background: var(--text-primary);
        color: white !important;
        text-decoration: none;
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        border-color: var(--text-primary);
    }

    /* 进度条现代化 */
    .stProgress > div > div > div {
        background: var(--accent) !important;
        border-radius: 4px !important;
        height: 4px !important;
    }

    /* 状态消息现代化 */
    .stSuccess {
        background: rgb(240 253 244) !important;
        border: 1px solid var(--success) !important;
        border-radius: var(--radius) !important;
        color: rgb(22 101 52) !important;
    }

    .stError {
        background: rgb(254 242 242) !important;
        border: 1px solid var(--error) !important;
        border-radius: var(--radius) !important;
        color: rgb(153 27 27) !important;
    }

    .stWarning {
        background: rgb(255 251 235) !important;
        border: 1px solid var(--warning) !important;
        border-radius: var(--radius) !important;
        color: rgb(146 64 14) !important;
    }

    /* 微动画 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .modern-title {
            font-size: 2rem;
        }

        .modern-card, .paper-card-modern {
            padding: 1rem;
            margin: 0.75rem 0;
        }

        .search-container {
            padding: 1.5rem;
            margin: 1.5rem 0;
        }

        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.75rem;
        }

        .paper-number-modern {
            position: static;
            display: inline-block;
            margin-bottom: 0.75rem;
        }

        .paper-title-modern {
            margin-right: 0;
        }

        .paper-meta-modern {
            flex-direction: column;
            gap: 0.5rem;
        }
    }

    /* 深色模式支持（可选） */
    @media (prefers-color-scheme: dark) {
        .stApp[data-theme="dark"] {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border: #334155;
            --border-light: #1e293b;
            --border-dark: #475569;
        }
    }

    /* 滚动条现代化 */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-dark);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* 焦点样式 */
    *:focus {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
    }

    button:focus,
    input:focus,
    select:focus {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
    }
    </style>
    """, unsafe_allow_html=True)


# 移除微妙效果函数，Canva风格已经足够美观


def display_header():
    """显示应用头部 - 现代极简风格。"""
    st.markdown("""
    <div class="modern-header">
        <div class="modern-title">
            🔬 AI Literature Review Agent
        </div>
        <div class="modern-subtitle">
            智能文献检索与分析系统
        </div>
        <div class="modern-description">
            基于大模型的学术研究助手，支持多数据源检索、智能分析与总结
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_metrics(results: Dict):
    """显示统计指标 - 现代极简风格。"""
    if results and "processed_papers" in results:
        papers = results["processed_papers"]

        # 使用现代化metrics-grid样式
        st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card-modern">
                <div class="metric-value-modern">{len(papers)}</div>
                <div class="metric-label-modern">📚 论文总数</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            full_text_count = sum(1 for p in papers if p.get("full_text_retrieved", False))
            st.markdown(f"""
            <div class="metric-card-modern">
                <div class="metric-value-modern">{full_text_count}</div>
                <div class="metric-label-modern">📄 全文获取</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            total_keywords = sum(len(p.get("keywords", [])) for p in papers)
            st.markdown(f"""
            <div class="metric-card-modern">
                <div class="metric-value-modern">{total_keywords}</div>
                <div class="metric-label-modern">🔍 关键词数</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            sources = set(p.get("source", "unknown") for p in papers)
            st.markdown(f"""
            <div class="metric-card-modern">
                <div class="metric-value-modern">{len(sources)}</div>
                <div class="metric-label-modern">🌐 数据源</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def display_paper_card(paper: Dict, index: int):
    """显示单个论文卡片 - 现代极简风格，使用Streamlit原生组件。"""
    # 处理作者列表
    authors = paper.get("authors", [])
    if authors:
        if len(authors) > 3:
            authors_str = f"{', '.join(authors[:3])} 等"
        else:
            authors_str = ", ".join(authors)
    else:
        authors_str = "未知作者"

    # 处理发布日期
    pub_date = paper.get("published_date")
    if pub_date:
        try:
            date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            date_str = date_obj.strftime("%Y/%m/%d")
        except:
            date_str = pub_date
    else:
        date_str = "未知日期"

    # 使用Streamlit原生组件构建卡片
    with st.container():
        # 开始卡片容器
        st.markdown('<div class="paper-card-modern fade-in-up">', unsafe_allow_html=True)

        # 论文编号（右上角）
        st.markdown(f'<div class="paper-number-modern">#{index}</div>', unsafe_allow_html=True)

        # 论文标题
        st.markdown(f'<div class="paper-title-modern">{paper.get("title", "未知标题")}</div>', unsafe_allow_html=True)

        # 元信息行
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"👥 **作者:** {authors_str}")
        with col2:
            st.markdown(f"📅 **日期:** {date_str}")
        with col3:
            st.markdown(f"📊 **来源:** {paper.get('source', 'unknown').upper()}")

        # 摘要
        summary = paper.get("ai_enhanced_summary", paper.get("original_summary", "暂无摘要"))
        if len(summary) > 300:
            summary = summary[:300] + "..."
        st.markdown(f"**摘要:** {summary}")

        # 关键词
        keywords = paper.get("keywords", [])
        if keywords:
            st.markdown("**关键词:**")
            # 使用columns来显示关键词标签
            keyword_cols = st.columns(min(len(keywords[:6]), 6))
            for i, kw in enumerate(keywords[:6]):
                with keyword_cols[i]:
                    st.markdown(f'<span class="keyword-tag-modern">{kw}</span>', unsafe_allow_html=True)

        # 操作按钮
        if paper.get("url") or paper.get("pdf_url"):
            st.markdown("**链接:**")
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])

            if paper.get("url"):
                with btn_col1:
                    st.markdown(f'<a href="{paper["url"]}" target="_blank" class="paper-link-modern">📄 查看原文</a>', unsafe_allow_html=True)

            if paper.get("pdf_url"):
                with btn_col2:
                    st.markdown(f'<a href="{paper["pdf_url"]}" target="_blank" class="paper-link-modern">📁 PDF下载</a>', unsafe_allow_html=True)

        # 结束卡片容器
        st.markdown('</div>', unsafe_allow_html=True)

        # 添加间距
        st.markdown("<br>", unsafe_allow_html=True)


def main():
    """主应用函数。"""
    # 页面配置
    st.set_page_config(
        page_title="AI Literature Review Agent",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 注入现代极简设计CSS
    inject_custom_css()

    # 显示头部
    display_header()

    # 侧边栏 - 现代极简风格
    with st.sidebar:
        with st.container():
            st.markdown('<div class="sidebar-modern">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title">🎛️ 检索配置</div>', unsafe_allow_html=True)

            # 数据源选择
            st.subheader("📚 数据源")
            sources = st.multiselect(
                "选择检索源",
                ["arxiv", "semantic_scholar"],
                default=["arxiv", "semantic_scholar"],
                help="选择要检索的学术数据库"
            )

            # 检索参数
            st.subheader("⚙️ 检索参数")
            max_papers = st.slider(
                "最大论文数",
                min_value=5,
                max_value=50,
                value=20,
                step=5,
                help="限制检索的最大论文数量"
            )

            retrieve_full_text = st.checkbox(
                "获取全文",
                value=False,
                help="尝试下载并处理PDF全文（可能较慢）"
            )

            # 时间范围
            st.subheader("📅 时间范围")
            col1, col2 = st.columns(2)
            with col1:
                year_start = st.number_input(
                    "起始年份",
                    min_value=1990,
                    max_value=2024,
                    value=2020,
                    step=1
                )
            with col2:
                year_end = st.number_input(
                    "结束年份",
                    min_value=1990,
                    max_value=2024,
                    value=2024,
                    step=1
                )

            st.markdown('</div>', unsafe_allow_html=True)

    # 主内容区
    main_container = st.container()

    with main_container:
        # 查询输入区 - 现代极简风格
        st.markdown('<div class="search-container">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            research_query = st.text_area(
                "🤖 智能研究查询",
                placeholder="请用自然语言描述您的研究需求，例如：\n• 我想了解最近三年人工智能在医疗诊断领域的应用进展\n• 寻找关于深度学习优化算法的最新研究，重点关注transformer架构\n• 查找2020年以来量子计算在密码学中的应用研究",
                help="系统会自动识别您的研究主题、时间范围和关注重点",
                height=100
            )

        with col2:
            st.write("")  # 空行对齐
            search_button = st.button(
                "🚀 开始检索",
                type="primary",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # 结果展示区
        if search_button and research_query:
            if not sources:
                st.error("❌ 请至少选择一个数据源！")
                return

            # 初始化会话状态
            if "results" not in st.session_state:
                st.session_state.results = None

            # 显示加载状态
            with st.spinner("🔄 正在检索和分析文献，请稍候..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # 更新进度
                    progress_bar.progress(20)
                    status_text.text("📡 初始化检索系统...")
                    time.sleep(0.5)

                    # 初始化agent
                    config = Config()
                    agent = LiteratureAgent(config=config)

                    progress_bar.progress(40)
                    status_text.text("🔍 检索相关文献...")
                    time.sleep(0.5)

                    # 执行检索 - 使用自然语言查询
                    results = asyncio.run(
                        agent.conduct_literature_review(
                            raw_query=research_query,
                            max_papers=max_papers,
                            sources=sources,
                            retrieve_full_text=retrieve_full_text,
                            year_start=year_start,
                            year_end=year_end
                        )
                    )

                    progress_bar.progress(80)
                    status_text.text("🤖 AI分析处理中...")
                    time.sleep(0.5)

                    # 存储结果
                    st.session_state.results = results

                    progress_bar.progress(100)
                    status_text.text("✅ 检索完成!")
                    time.sleep(0.3)

                    # 清理进度指示器
                    progress_bar.empty()
                    status_text.empty()

                except Exception as e:
                    st.error(f"❌ 检索过程中出现错误: {str(e)}")
                    return

        # 显示结果
        if st.session_state.get("results"):
            results = st.session_state.results

            st.success(f"✅ 成功检索到 {results.get('num_papers_processed', 0)} 篇相关文献")

            # 显示行动计划
            if results.get("action_plan"):
                st.subheader("🤖 AI生成的行动计划")
                action_plan = results["action_plan"]

                # 创建两列布局显示行动计划
                col1, col2 = st.columns(2)
                for i, step in enumerate(action_plan):
                    if i % 2 == 0:
                        with col1:
                            st.info(f"**步骤 {i+1}:** {step}")
                    else:
                        with col2:
                            st.info(f"**步骤 {i+1}:** {step}")

                st.caption("💡 此计划由AI根据您的查询自动生成，展示了文献检索和分析的主要步骤")
                st.divider()

            # 显示统计指标
            display_metrics(results)

            # 显示论文列表
            if results.get("processed_papers"):
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.subheader("📚 检索结果")

                papers = results["processed_papers"]

                # 排序选项
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"共找到 **{len(papers)}** 篇相关论文")
                with col2:
                    sort_by = st.selectbox(
                        "排序方式",
                        ["默认", "按时间降序", "按标题"],
                        index=0
                    )

                # 排序处理
                if sort_by == "按时间降序":
                    papers = sorted(
                        papers,
                        key=lambda x: x.get("published_date", ""),
                        reverse=True
                    )
                elif sort_by == "按标题":
                    papers = sorted(
                        papers,
                        key=lambda x: x.get("title", "").lower()
                    )

                st.markdown('</div>', unsafe_allow_html=True)

                # 显示论文卡片
                for i, paper in enumerate(papers, 1):
                    display_paper_card(paper, i)

            else:
                st.warning("⚠️ 未找到相关文献，请尝试调整搜索关键词或扩大时间范围。")


if __name__ == "__main__":
    main()