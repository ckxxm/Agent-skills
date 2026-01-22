#!/usr/bin/env python3
"""
Fetch AI Developer News - 开发者版

This script helps gather the latest AI developer-focused news and updates,
organizing them into categories: Developer Tools & APIs, Agent Frameworks,
SDK & Library Releases, Technical Research, and Open Source Projects.

Target audience: AI application developers and agent researchers.
"""

import sys
from datetime import datetime, timedelta


def get_week_range():
    """Get the current week's date range for search queries."""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_str = start_of_week.strftime("%Y-%m-%d")
    end_str = end_of_week.strftime("%Y-%m-%d")

    return start_str, end_str, today.strftime("%Y-%m-%d")


def generate_search_queries(category: str, start_date: str, end_date: str) -> list[str]:
    """Generate search queries for different AI developer news categories."""

    queries = {
        "api_tools": [
            f'"OpenAI API update" OR "Anthropic Claude API" OR "Gemini API release" {start_date} {end_date}',
            f'SDK release OR developer console OR endpoint changes {start_date} {end_date}',
            f'pricing update OR rate limit OR API features {start_date} {end_date}',
        ],
        "agent_frameworks": [
            f'"agent framework" OR "agent skills" OR "function calling" OR "tool use" {start_date} {end_date}',
            f'"Claude Skills" OR "OpenAI function calling" OR AutoGen OR "LangChain agent" OR CrewAI {start_date} {end_date}',
            f'"multi-agent system" OR "agent orchestration" OR "agent deployment" {start_date} {end_date}',
        ],
        "libraries": [
            f'"LangChain release" OR "LlamaIndex update" OR SDK release OR library launch {start_date} {end_date}',
            f'Python SDK OR JavaScript SDK OR TypeScript agent framework {start_date} {end_date}',
            f'version release AND AI framework {start_date} {end_date}',
        ],
        "technical": [
            f'"prompt engineering guide" OR "RAG tutorial" OR "fine-tuning best practices" {start_date} {end_date}',
            f'LLM evaluation OR agent testing OR benchmarking tools {start_date} {end_date}',
            f'technical blog AND AI development OR engineering {start_date} {end_date}',
        ],
        "opensource": [
            f'"open-source LLM" OR "GitHub AI project" OR "agent framework open source" {start_date} {end_date}',
            f'Hugging Face release OR model repository OR developer tool {start_date} {end_date}',
            f'GitHub trending AI/ML {start_date} {end_date}',
        ]
    }

    return queries.get(category, [])


def print_markdown_template(start_date: str, end_date: str, today: str):
    """Print the markdown template for the weekly developer report."""

    print(f"""# AI 开发者周报

**本周时间**: {start_date} 至 {end_date}
**生成时间**: {today}

> 面向 AI 应用开发者和智能体研发人员的技术情报周报

---

## 🛠️ 开发工具与平台更新

### API 更新

*搜索查询:*
```
{generate_search_queries("api_tools", start_date, end_date)[0]}
{generate_search_queries("api_tools", start_date, end_date)[1]}
{generate_search_queries("api_tools", start_date, end_date)[2]}
```

*结果:*
<!-- 添加 API 更新信息 -->

---

## 🤖 Agent 框架与能力

### Agent Skills 与工具调用

*搜索查询:*
```
{generate_search_queries("agent_frameworks", start_date, end_date)[0]}
{generate_search_queries("agent_frameworks", start_date, end_date)[1]}
{generate_search_queries("agent_frameworks", start_date, end_date)[2]}
```

*结果:*
<!-- 添加 Agent 框架更新信息 -->

---

## 📦 SDK 与库发布

*搜索查询:*
```
{generate_search_queries("libraries", start_date, end_date)[0]}
{generate_search_queries("libraries", start_date, end_date)[1]}
{generate_search_queries("libraries", start_date, end_date)[2]}
```

*结果:*
<!-- 添加 SDK 和库发布信息 -->

---

## 🔬 技术研究与最佳实践

*搜索查询:*
```
{generate_search_queries("technical", start_date, end_date)[0]}
{generate_search_queries("technical", start_date, end_date)[1]}
{generate_search_queries("technical", start_date, end_date)[2]}
```

*结果:*
<!-- 添加技术研究和最佳实践信息 -->

---

## 💡 开源项目与工具

*搜索查询:*
```
{generate_search_queries("opensource", start_date, end_date)[0]}
{generate_search_queries("opensource", start_date, end_date)[1]}
{generate_search_queries("opensource", start_date, end_date)[2]}
```

*结果:*
<!-- 添加开源项目和工具信息 -->

---

## 📊 行业动态

*搜索查询:*
```
AI platform policy changes OR developer tools acquisition {start_date} {end_date}
AI regulation impacting developers {start_date} {end_date}
```

*结果:*
<!-- 添加行业动态信息 -->

---

## 🔑 本周开发者重点关注

1.
2.
3.

---

## 📚 推荐阅读

-
-

---
*由 AI Weekly Skill 自动生成 - 开发者版*
""")


def main():
    """Main execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("\nUsage: python3 fetch_ai_news.py")
        print("Output: Markdown template with search queries for the current week")
        print("\nCategories:")
        print("  - API & Developer Tools")
        print("  - Agent Frameworks & Skills")
        print("  - SDK & Library Releases")
        print("  - Technical Research & Best Practices")
        print("  - Open Source & Tools")
        sys.exit(0)

    start_date, end_date, today = get_week_range()
    print_markdown_template(start_date, end_date, today)


if __name__ == "__main__":
    main()
