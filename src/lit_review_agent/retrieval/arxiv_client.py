"""ArXiv API client for literature retrieval."""

import asyncio
import re
from datetime import datetime
from typing import List, Optional

import arxiv
from ..utils.logger import LoggerMixin
from .base_retriever import BaseRetriever, LiteratureItem


class ArxivClient(BaseRetriever, LoggerMixin):
    """Client for retrieving literature from arXiv."""

    # 中文关键词到英文的映射
    CHINESE_TO_ENGLISH = {
        # 基础术语
        "深度学习": "deep learning",
        "机器学习": "machine learning",
        "人工智能": "artificial intelligence",
        "神经网络": "neural network",
        "卷积神经网络": "convolutional neural network",
        "循环神经网络": "recurrent neural network",
        "transformer": "transformer",
        "注意力机制": "attention mechanism",
        "自然语言处理": "natural language processing",
        "计算机视觉": "computer vision",
        "强化学习": "reinforcement learning",

        # 优化相关
        "优化算法": "optimization algorithm",
        "梯度下降": "gradient descent",
        "反向传播": "backpropagation",
        "损失函数": "loss function",
        "正则化": "regularization",
        "批量归一化": "batch normalization",
        "学习率": "learning rate",

        # 应用领域
        "医疗": "medical",
        "诊断": "diagnosis",
        "图像识别": "image recognition",
        "语音识别": "speech recognition",
        "推荐系统": "recommendation system",
        "自动驾驶": "autonomous driving",

        # 研究相关
        "最新研究": "recent research",
        "综述": "survey",
        "算法": "algorithm",
        "模型": "model",
        "方法": "method",
        "技术": "technique",
        "应用": "application",
        "性能": "performance",
        "准确率": "accuracy",
        "效果": "effectiveness"
    }

    def __init__(self, max_results: int = 100, **kwargs):
        """
        Initialize the ArXiv client.

        Args:
            max_results: Default maximum results per query
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.max_results = max_results

        # Configure ArXiv client with better timeout and retry settings
        self.client = arxiv.Client(
            page_size=100,  # Fetch more results per request
            delay_seconds=3,  # Respect rate limits
            num_retries=3  # Retry failed requests
        )

        self.logger.info(
            f"Initialized ArXiv client with max_results={max_results}, "
            f"page_size=100, delay=3s, retries=3")

    def get_source_name(self) -> str:
        """Get the source name."""
        return "arxiv"

    def translate_chinese_query(self, query: str) -> str:
        """
        将中文查询翻译为英文查询

        Args:
            query: 原始查询字符串

        Returns:
            翻译后的英文查询字符串
        """
        if not query or not isinstance(query, str):
            return query

        # 检查是否包含中文字符
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in query)
        if not has_chinese:
            return query

        # 记录原始查询
        self.logger.info(f"Translating Chinese query: '{query}'")

        # 简单的关键词替换翻译
        translated_query = query
        for chinese, english in self.CHINESE_TO_ENGLISH.items():
            if chinese in translated_query:
                translated_query = translated_query.replace(chinese, english)
                self.logger.info(f"Replaced '{chinese}' with '{english}'")

        # 移除常见的中文连接词和标点
        chinese_stopwords = ["的", "在", "中", "与", "和", "或", "关于", "对于", "基于", "通过", "使用", "采用", "研究", "分析", "方法", "技术", "算法",
                             "模型", "系统", "应用", "实现", "设计", "开发", "提出", "改进", "优化", "评估", "实验", "结果", "效果", "性能", "比较", "分析", "讨论", "总结", "结论"]
        for stopword in chinese_stopwords:
            translated_query = translated_query.replace(stopword, " ")

        # 清理多余的空格
        translated_query = " ".join(translated_query.split())

        # 如果翻译后为空或只有标点，使用默认查询
        if not translated_query.strip() or len(translated_query.strip()) < 3:
            translated_query = "machine learning"
            self.logger.warning(
                f"Translation resulted in empty query, using default: '{translated_query}'")

        self.logger.info(f"Final translated query: '{translated_query}'")
        return translated_query

    async def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
        sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending,
        **kwargs,
    ) -> List[LiteratureItem]:
        """
        Search ArXiv for papers.

        Args:
            query: Search query
            max_results: Maximum number of results
            sort_by: Sort criterion
            sort_order: Sort order
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        try:
            # 处理中文查询
            original_query = query
            if isinstance(query, str):
                # 自动翻译中文查询
                query = self.translate_chinese_query(query)

                # 记录查询信息
                if original_query != query:
                    self.logger.info(
                        f"Searching ArXiv: original_query='{original_query}' -> translated_query='{query}', max_results={max_results}"
                    )
                else:
                    self.logger.info(
                        f"Searching ArXiv: query='{query}', max_results={max_results}"
                    )

            # Create search object
            search = arxiv.Search(
                query=query,
                max_results=min(max_results, self.max_results),
                sort_by=sort_by,
                sort_order=sort_order,
            )

            # Execute search with timeout
            def search_arxiv():
                try:
                    return list(self.client.results(search))
                except Exception as e:
                    self.logger.error(f"ArXiv API error: {e}")
                    return []

            loop = asyncio.get_event_loop()
            results = await asyncio.wait_for(
                loop.run_in_executor(None, search_arxiv),
                timeout=45  # 45秒超时，给ArXiv API足够时间
            )

            # Convert to LiteratureItem objects
            literature_items = []
            for result in results:
                item = self._convert_arxiv_result(result)
                literature_items.append(item)

            self.logger.info(
                f"Retrieved {len(literature_items)} papers from ArXiv")
            return literature_items

        except asyncio.TimeoutError:
            self.logger.error("ArXiv search timed out")
            raise Exception("ArXiv search timed out after 45 seconds")
        except Exception as e:
            self.logger.error(f"Error searching ArXiv: {e}")
            raise Exception(f"ArXiv search failed: {e}")

    async def get_by_id(self, item_id: str) -> Optional[LiteratureItem]:
        """
        Retrieve a specific paper by ArXiv ID.

        Args:
            item_id: ArXiv ID (e.g., '2301.12345')

        Returns:
            Literature item if found, None otherwise
        """
        try:
            self.logger.info(f"Retrieving ArXiv paper by ID: {item_id}")

            # Create search for specific ID
            search = arxiv.Search(id_list=[item_id])

            # Execute search asynchronously
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, lambda: list(self.client.results(search))
            )

            if results:
                item = self._convert_arxiv_result(results[0])
                self.logger.info(f"Found ArXiv paper: {item.title}")
                return item
            else:
                self.logger.warning(f"ArXiv paper not found: {item_id}")
                return None

        except Exception as e:
            self.logger.error(f"Error retrieving ArXiv paper {item_id}: {e}")
            return None

    async def search_by_category(
        self, category: str, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search ArXiv by category.

        Args:
            category: ArXiv category (e.g., 'cs.AI', 'cs.LG')
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        query = f"cat:{category}"
        return await self.search(query, max_results, **kwargs)

    async def search_by_author(
        self, author: str, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search ArXiv by author.

        Args:
            author: Author name
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        query = f"au:{author}"
        return await self.search(query, max_results, **kwargs)

    async def search_recent(
        self, query: str, days: int = 30, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search for recent papers.

        Args:
            query: Search query
            days: Number of days to look back
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of recent literature items
        """
        # ArXiv doesn't support date filtering in the API directly,
        # so we'll retrieve more results and filter client-side
        expanded_results = max_results * 3
        all_items = await self.search(query, expanded_results, **kwargs)

        # Filter by date
        cutoff_date = datetime.utcnow()
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)

        recent_items = self.filter_by_date(all_items, start_date=cutoff_date)

        return recent_items[:max_results]

    def _convert_arxiv_result(self, arxiv_result) -> LiteratureItem:
        """
        Convert ArXiv result to LiteratureItem.

        Args:
            arxiv_result: ArXiv API result object

        Returns:
            LiteratureItem object
        """
        # Extract ArXiv ID from URL
        arxiv_id = arxiv_result.entry_id.split("/")[-1]

        # Extract authors
        authors = [str(author) for author in arxiv_result.authors]

        # Extract categories
        categories = [str(cat) for cat in arxiv_result.categories]

        # Create LiteratureItem
        return LiteratureItem(
            id=f"arxiv:{arxiv_id}",
            title=arxiv_result.title,
            authors=authors,
            abstract=arxiv_result.summary,
            publication_date=arxiv_result.published,
            journal=arxiv_result.journal_ref,
            doi=arxiv_result.doi,
            arxiv_id=arxiv_id,
            url=arxiv_result.entry_id,
            pdf_url=arxiv_result.pdf_url,
            categories=categories,
            source="arxiv",
            metadata={
                "updated": (
                    arxiv_result.updated.isoformat() if arxiv_result.updated else None
                ),
                "comment": arxiv_result.comment,
                "primary_category": (
                    str(arxiv_result.primary_category)
                    if arxiv_result.primary_category
                    else None
                ),
                "links": (
                    [str(link) for link in arxiv_result.links]
                    if arxiv_result.links
                    else []
                ),
            },
        )

    def _generate_mock_data(self, query: str, max_results: int) -> List[LiteratureItem]:
        """
        生成模拟数据作为网络失败时的回退方案

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            模拟的文献项目列表
        """
        from datetime import datetime, timezone
        import uuid

        mock_papers = []

        # 基于查询生成相关的模拟论文
        topics = {
            "machine learning": [
                ("Deep Learning Advances in Neural Networks",
                 ["Smith, J.", "Johnson, A.", "Brown, K."]),
                ("Reinforcement Learning for Autonomous Systems",
                 ["Davis, M.", "Wilson, R."]),
                ("Transfer Learning in Computer Vision", [
                 "Garcia, L.", "Martinez, C.", "Lopez, D."]),
            ],
            "quantum computing": [
                ("Quantum Algorithms for Optimization Problems",
                 ["Chen, W.", "Zhang, Y.", "Liu, X."]),
                ("Quantum Error Correction in NISQ Devices",
                 ["Anderson, P.", "Taylor, S."]),
                ("Quantum Machine Learning Applications",
                 ["Kumar, R.", "Patel, N.", "Singh, A."]),
            ],
            "artificial intelligence": [
                ("Explainable AI in Healthcare Applications",
                 ["Thompson, E.", "White, M."]),
                ("Large Language Models and Reasoning",
                 ["Lee, H.", "Kim, J.", "Park, S."]),
                ("AI Ethics and Fairness in Decision Making",
                 ["Miller, D.", "Jones, B.", "Clark, R."]),
            ]
        }

        # 选择相关主题
        selected_topics = []
        query_lower = query.lower()
        for topic, papers in topics.items():
            if any(word in query_lower for word in topic.split()):
                selected_topics.extend(papers)

        # 如果没有匹配的主题，使用通用主题
        if not selected_topics:
            selected_topics = [
                (f"Research on {query.title()}: A Comprehensive Survey", [
                 "Author, A.", "Researcher, B."]),
                (f"Novel Approaches to {query.title()}", [
                 "Expert, C.", "Scholar, D."]),
                (f"Applications of {query.title()} in Modern Technology", [
                 "Scientist, E.", "Professor, F."]),
            ]

        # 生成指定数量的模拟论文
        for i in range(min(max_results, len(selected_topics))):
            if i < len(selected_topics):
                title, authors = selected_topics[i]
            else:
                title = f"Advanced Studies in {query.title()} - Part {i+1}"
                authors = [f"Author{i+1}, X.", f"Researcher{i+1}, Y."]

            # 生成模拟ID
            mock_id = f"mock:{uuid.uuid4().hex[:8]}"

            # 生成模拟摘要
            abstract = f"This paper presents a comprehensive study on {query}. " \
                f"We propose novel methodologies and demonstrate significant improvements " \
                f"over existing approaches. Our experimental results show promising " \
                f"applications in various domains. The findings contribute to the " \
                f"advancement of {query} research and open new avenues for future work."

            # 创建模拟的LiteratureItem
            mock_paper = LiteratureItem(
                id=mock_id,
                title=title,
                authors=authors,
                abstract=abstract,
                publication_date=datetime.now(timezone.utc),
                journal="arXiv preprint",
                arxiv_id=f"2024.{1000+i:04d}",
                url=f"https://arxiv.org/abs/2024.{1000+i:04d}",
                pdf_url=f"https://arxiv.org/pdf/2024.{1000+i:04d}.pdf",
                categories=["cs.AI", "cs.LG"],
                source="arxiv",
                metadata={
                    "mock_data": True,
                    "generated_for_query": query,
                    "note": "This is mock data generated due to network connectivity issues"
                }
            )

            mock_papers.append(mock_paper)

        self.logger.info(
            f"Generated {len(mock_papers)} mock papers for query: {query}")
        return mock_papers

    def get_supported_categories(self) -> List[str]:
        """
        Get list of supported ArXiv categories.

        Returns:
            List of category codes
        """
        return [
            # Computer Science
            "cs.AI",  # Artificial Intelligence
            "cs.CL",  # Computation and Language
            "cs.CV",  # Computer Vision and Pattern Recognition
            "cs.LG",  # Machine Learning
            "cs.NE",  # Neural and Evolutionary Computing
            "cs.RO",  # Robotics
            # Statistics
            "stat.ML",  # Machine Learning
            "stat.AP",  # Applications
            # Mathematics
            "math.OC",  # Optimization and Control
            "math.ST",  # Statistics Theory
            # Physics
            "physics.data-an",  # Data Analysis
            # Quantitative Biology
            "q-bio.QM",  # Quantitative Methods
            # Economics
            "econ.EM",  # Econometrics
        ]
