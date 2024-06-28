import json
from typing import Optional, Dict, List, Tuple, Any
from chatways.bot.utils import BaseChatBot
from chatways.tool.utils import TOOL_REGISTRY

ARXIV_SYSTEM_PROMPT = "你擅长给用户推荐学术论文。"

ARXIV_SEARCH_PROMPT = """任务
根据用户问题提取关键信息，用于论文搜索。

输入
用户问题或陈述（字符串）。

输出
JSON格式，包含以下字段：
{
    "research_field": ["<topic1>", "<topic2>"],
    "authors": ["<author1>", "<author2>"],
    "search_order": "<sort type>"
}

字段说明
research_field：英文研究主题（必须为英文），可以为空。
authors：英文论文作者（必须为英文），可以为空。
search_order：检索方法，值为 "Latest"（按最新排序）或 "Relevance"（按相关度排序）。
"""

ARXIV_CHAT_TEMPLATE = """请根据arXiv论文候选集来回答问题，不要编造，若arXiv论文候选集为空，提醒我检查arXiv服务是否可用。

arXiv论文候选集：

{content}

问题：

{message}
"""

PAPER_CARD_TEMPLATE = """
### [{index}. {title}]({pdf_url})

**Authors:** {authors}

**Abstract:** {abstract}

"""

PAPER_CARD_MARKDOWN = """
<div style="flex: 1; overflow-y: auto;">
{content}
</div>
"""


class ArxivChatBot(BaseChatBot):

    def __init__(self, llm_config: Optional[dict] = None) -> None:
        super().__init__(llm_config)
        self.tool = TOOL_REGISTRY["arxiv"]()

    def _search_from_arxiv(
        self,
        message: str,
        history: List[Tuple[str, str]],
        generation_config: Optional[Dict] = None,
        max_results: int = 5,
    ) -> Tuple[str, str]:
        response = self._chat(
            message=message,
            history=history,
            system_prompt=ARXIV_SEARCH_PROMPT,
            generation_config=generation_config,
            stream=False,
        )
        papers = self.tool.call(response, max_results=max_results)
        return papers, response

    def _chat(
        self,
        message: str,
        history: List[Tuple[str, str]],
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict] = None,
        stream: bool = True,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if len(history) > 0:
            for query, response in history:
                messages.append({"role": "user", "content": query})
                messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": message})
        if stream:
            response = self.llm.invoke_stream(messages, generation_config)
        else:
            response = self.llm.invoke(messages, generation_config)
        return response

    def chat(
        self,
        message: str,
        history_chat: List[Tuple[str, str]],
        history_search: List[Tuple[str, str]],
        generation_config: Optional[Dict] = None,
        max_results: int = 5,
        stream: bool = True,
    ) -> Tuple[str, str, str]:
        papers, paper_search_query = self._search_from_arxiv(
            message, history_search, generation_config, max_results
        )
        paper_cards = self._generate_paper_cards(papers)
        messaeg_for_llm = self._prepare_message_for_llm(message, papers)
        response = self._chat(
            message=messaeg_for_llm,
            history=history_chat,
            system_prompt=ARXIV_SYSTEM_PROMPT,
            generation_config=generation_config,
            stream=stream,
        )
        return response, paper_cards, paper_search_query

    def _generate_paper_cards(self, papers: Any) -> str:
        if not papers:
            return ""
        papers = json.loads(papers)
        paper_cards = ""
        for index, paper in enumerate(papers):
            paper_cards += PAPER_CARD_TEMPLATE.format(
                index=index + 1,
                title=paper["title"],
                authors=", ".join(paper["authors"]),
                abstract=paper["summary"],
                pdf_url=paper["pdf_url"],
            )
        paper_cards = PAPER_CARD_MARKDOWN.format(content=paper_cards)
        return paper_cards

    def _prepare_message_for_llm(self, message: str, papers: Any) -> str:
        if not papers:
            return message
        papers = json.loads(papers)
        content = ""
        for paper in papers:
            content += "题目：{title}\n".format(title=paper["title"])
            content += "作者：{authors}\n".format(authors=", ".join(paper["authors"]))
            content += "摘要：{abstract}\n\n".format(abstract=paper["summary"])

        message = ARXIV_CHAT_TEMPLATE.format(content=content, message=message)
        return message
