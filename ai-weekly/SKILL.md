---
name: ai-weekly
description: Weekly intelligence report for AI application developers and AI agent researchers. Focus on developer tools, SDK updates, agent frameworks, API releases, open-source projects, and platform capabilities. Target audience is engineers building AI applications, agents, and integrated systems. Use when users request AI development news, agent framework updates, API releases, or developer-focused AI industry insights. All output in Chinese.
---

# AI Weekly - 开发者版

面向AI应用开发者和智能体研发人员的周报。

## 目标受众

- AI应用开发者
- 智能体(Agent)研发人员
- AI平台工程师
- LLM集成开发者

## Quick Start

When a user requests AI industry news or weekly updates:

1. **Determine time scope**: Use current week (Monday to Sunday) unless user specifies otherwise
2. **Gather news**: Use WebSearch tool to find recent AI developments across **developer-focused categories**
3. **Compile report**: Organize findings into structured Markdown format in **Chinese (中文)**
4. **Prioritize**: Developer tools, agent frameworks, API updates, SDK releases over general industry news
5. **Cite sources**: Include source links for all news items with format: [来源](url) or [Source](url)

For direct command execution, run the helper script:
```bash
python3 scripts/fetch_ai_news.py
```

## Report Structure

Output a Markdown report in Chinese with these sections:

### 🛠️ 开发工具与平台更新 (Developer Tools & Platform Updates)
**CRITICAL SECTION** - API releases, SDK updates, developer console changes, new endpoints, pricing changes
- OpenAI API updates (new models, endpoints, features)
- Anthropic Claude API/Claude Code changes
- Google Gemini API updates
- Agent framework releases (LangChain, AutoGen, CrewAI, etc.)
- Development tools and IDE integrations

### 🤖 Agent 框架与能力 (Agent Frameworks & Capabilities)
**CRITICAL SECTION** - Agent-related features and frameworks
- Agent Skills (e.g., Claude Skills, OpenAI function calling updates)
- Multi-agent systems and orchestration
- Tool use and function calling enhancements
- Agent evaluation and testing frameworks
- Agent deployment platforms

### 📦 SDK 与库发布 (SDK & Library Releases)
New libraries, SDK updates, or major version releases
- Python/JavaScript/Go SDKs
- Framework updates (LangChain, LlamaIndex, etc.)
- Open-source agent frameworks
- Integration libraries

### 🔬 技术研究与最佳实践 (Technical Research & Best Practices)
Developer-focused research papers and technical blog posts
- Prompt engineering techniques
- RAG (Retrieval-Augmented Generation) improvements
- Fine-tuning methods and tools
- Evaluation and benchmarking tools
- Performance optimization techniques

### 💡 开源项目与工具 (Open Source & Tools)
Notable open-source projects and developer tools
- New open-source models
- Developer tools and utilities
- Community projects and repositories

### 📊 行业动态 (Industry News)
**LOWER PRIORITY** - Only major industry shifts affecting developers
- Platform policy changes
- Major acquisitions affecting developer tools
- Regulatory changes impacting AI development

## Search Strategy

**CRITICAL: Prioritize developer-centric sources and keywords**

### Primary Search Categories

**1. Developer Tools & APIs**
```
"OpenAI API update" OR "Anthropic Claude API" OR "Gemini API release" OR "SDK release"
"developer console" OR "API documentation" OR "endpoint changes"
"pricing update" OR "rate limit" OR "API features"
```

**2. Agent Frameworks & Skills**
```
"agent framework" OR "agent skills" OR "function calling" OR "tool use"
"Claude Skills" OR "OpenAI function calling" OR "AutoGen" OR "LangChain agent" OR "CrewAI"
"multi-agent system" OR "agent orchestration" OR "agent deployment"
```

**3. Libraries & SDKs**
```
"LangChain release" OR "LlamaIndex update" OR "SDK release" OR "library launch"
"Python SDK" OR "JavaScript SDK" OR "TypeScript agent framework"
"version release" OR "major update" AND "AI framework"
```

**4. Technical Content**
```
"prompt engineering guide" OR "RAG tutorial" OR "fine-tuning best practices"
"LLM evaluation" OR "agent testing" OR "benchmarking tools"
"technical blog" AND "AI development" OR "engineering"
```

**5. Open Source**
```
"open-source LLM" OR "GitHub AI project" OR "agent framework open source"
"Hugging Face release" OR "model repository" OR "developer tool"
```

### Key Sources for Developer Intelligence

**Official Developer Platforms:**
- OpenAI Developer News (platform.openai.com)
- Anthropic Claude Developer Blog (developer.anthropic.com)
- Google AI/ML Developer Blog
- Hugging Face Blog

**Technical Publications:**
- towardsdatascience.com (Medium)
- InfoQ
- The New Stack
- Dev.to

**Community Platforms:**
- GitHub Trending (AI/ML category)
- Hacker News
- Reddit (r/LocalLLaMA, r/MachineLearning)

**Agent-Focused Sources:**
- LangChain Blog
- LlamaIndex Blog
- AutoGen Documentation
- CrewAI Blog

## Output Format

**CRITICAL: All reports MUST be in Chinese (中文)**

Use the template structure in `references/template.md`. Each news item should include:
- Brief headline/title in bold (中文标题)
- One-sentence summary in Chinese (中文摘要)
- **Developer impact**: Why this matters to developers (开发者影响)
- Source link: [来源](url) or [Source](url)

For example:
```markdown
- **Claude Skills 发布** - Anthropic 推出 Agent Skills，将 Claude 从编程助手转变为通用 Agent，支持模块化任务组件和命令行自动化。
  - **开发者影响**: 可构建能执行实际任务的 AI Agent，支持跨平台部署（Claude.ai/Claude Code/API）
  - [来源](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
```

## Key Principles

1. **Developer-First**: Prioritize information that helps developers build, integrate, and deploy AI applications
2. **Actionable Intelligence**: Focus on updates developers can act on (API changes, new tools, framework updates)
3. **Technical Depth**: Include technical details, version numbers, API endpoints, code examples when available
4. **Agent-Centric**: Pay special attention to agent frameworks, multi-agent systems, and agentic AI capabilities
5. **Ignore Fluff**: Skip celebrity news, general hype, non-technical announcements unless they impact developers

## Resources

### scripts/fetch_ai_news.py
Helper script that generates a Markdown template with pre-filled search queries for the current week. Execute directly to get started, or use as reference for query structure.

### references/sources.md
Comprehensive list of recommended AI news sources and search keywords organized by category. **Now includes developer-focused sources**.

### references/template.md
Standard Markdown template for the weekly report format. **Updated to include developer-centric sections**.
