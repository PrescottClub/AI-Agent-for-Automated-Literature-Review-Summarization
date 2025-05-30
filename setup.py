#!/usr/bin/env python3
"""
AI Literature Review & Summarization Agent
智能文献综述与总结代理
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 读取requirements.txt
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="tsearch-literature-agent",
    version="1.0.0",
    author="Terence Qin",
    author_email="prescottchun@163.com",
    description="AI Agent for Automated Literature Review & Summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Researchers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tsearch=lit_review_agent.cli:main",
            "tsearch-api=lit_review_agent.api_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lit_review_agent": ["config/*.yaml", "templates/*.txt"],
    },
    zip_safe=False,
)
