"""Streamlit web interface for Literature Review Agent."""

from lit_review_agent.utils.config import Config
from lit_review_agent.agent import LiteratureAgent
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


def load_css(file_path: Path) -> str:
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.warning(f"Custom CSS file not found at {file_path}")
        return ""
    except Exception as e:
        st.error(f"Error loading CSS file {file_path}: {e}")
        return ""


def inject_custom_css():
    """注入2024年现代极简设计CSS样式。"""
    # 构建到 assets/styles.css 的路径
    # __file__ 是 app.py 的路径
    # .parent 是 src/lit_review_agent/
    # .parent.joinpath("assets", "styles.css") 将指向 src/lit_review_agent/assets/styles.css
    css_file_path = Path(__file__).parent / "assets" / "styles.css"

    custom_css = load_css(css_file_path)
    if custom_css:
        st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
    else:
        # Fallback or default message if CSS is essential and not loaded
        st.info(
            "Attempted to load custom styles, but the CSS file was empty or not found.")


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
            full_text_count = sum(1 for p in papers if p.get(
                "full_text_retrieved", False))
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
        st.markdown('<div class="paper-card-modern fade-in-up">',
                    unsafe_allow_html=True)

        # 论文编号（右上角）
        st.markdown(
            f'<div class="paper-number-modern">#{index}</div>', unsafe_allow_html=True)

        # 论文标题
        st.markdown(
            f'<div class="paper-title-modern">{paper.get("title", "未知标题")}</div>', unsafe_allow_html=True)

        # 元信息行
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"👥 **作者:** {authors_str}")
        with col2:
            st.markdown(f"📅 **日期:** {date_str}")
        with col3:
            st.markdown(f"📊 **来源:** {paper.get('source', 'unknown').upper()}")

        # 摘要
        summary = paper.get("ai_enhanced_summary",
                            paper.get("original_summary", "暂无摘要"))
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
                    st.markdown(
                        f'<span class="keyword-tag-modern">{kw}</span>', unsafe_allow_html=True)

        # 操作按钮
        if paper.get("url") or paper.get("pdf_url"):
            st.markdown("**链接:**")
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])

            if paper.get("url"):
                with btn_col1:
                    st.markdown(
                        f'<a href="{paper["url"]}" target="_blank" class="paper-link-modern">📄 查看原文</a>', unsafe_allow_html=True)

            if paper.get("pdf_url"):
                with btn_col2:
                    st.markdown(
                        f'<a href="{paper["pdf_url"]}" target="_blank" class="paper-link-modern">📁 PDF下载</a>', unsafe_allow_html=True)

        # 结束卡片容器
        st.markdown('</div>', unsafe_allow_html=True)

        # 添加间距
        st.markdown("<br>", unsafe_allow_html=True)


@st.cache_resource
def get_agent():
    """Cached function to initialize and get the LiteratureAgent."""
    app_config = Config()
    return LiteratureAgent(config=app_config)


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
            st.markdown('<div class="sidebar-title">🎛️ 检索配置</div>',
                        unsafe_allow_html=True)

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
                    agent = get_agent()

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

            st.success(
                f"✅ 成功检索到 {results.get('num_papers_processed', 0)} 篇相关文献")

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
                st.markdown('<div class="modern-card">',
                            unsafe_allow_html=True)
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
