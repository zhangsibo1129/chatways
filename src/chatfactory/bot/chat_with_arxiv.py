import json
from typing import Optional, Dict, List, Tuple, Any
from chatfactory.llm.utils import LLM_REGISTRY
from chatfactory.tool.utils import TOOL_REGISTRY
from chatfactory.log import logger

ARXIV_SYSTEM_PROMPT = "你负责根据用户问题给出论文推荐，可以使用arXiv论文搜索引擎，根据论文候选集来回答，不要编造答案。"

ARXIV_SEARCH_PROMPT = """你的任务是从对话中提取以下三个字段信息，用于学术论文的搜索：

1. research_field：论文的研究主题或领域。以字符串列表形式表示，例如 ["machine learning", "medical image analysis"]。
2. authors：论文作者。以字符串列表形式表示，例如 ["John Doe", "Jane Smith"]。
3. search_order：检索方法，只能取值为 "Latest" 或 "Relevance"。其中：
    - "Latest" 表示按最新排序。
    - "Relevance" 表示按相关度排序。

注意事项：

- 专注于提取信息，不要直接回答对话中的问题。
- 确保提取的字段内容为英文。
- 信息缺失时字段可以为空。

输出格式：

请按照以下JSON格式输出提取的信息：

{
  "research_field": ["example field"],
  "authors": ["example author"],
  "search_order": "Relevance"
}

示例：

输入对话：
User: I'm looking for the latest papers in machine learning and data mining. Can you also find papers by Andrew Ng?

输出：
{
  "research_field": ["machine learning", "data mining"],
  "authors": ["Andrew Ng"],
  "search_order": "Latest"
}

输入对话：
User: Could you find relevant papers by Jane Smith on natural language processing?

输出：
{
  "research_field": ["natural language processing"],
  "authors": ["Jane Smith"],
  "search_order": "Relevance"
}

"""

ARXIV_CHAT_TEMPLATE = """论文候选集：

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

class ArxivChatBot:
    def __init__(self, llm_config: Optional[dict] = None) -> None:
        llm_engine, model, model_config= self.parse_llm_config(llm_config)
        self.setup_model(llm_engine, model, model_config)
        self.tool = TOOL_REGISTRY['arxiv']()
        
    def parse_llm_config(self, llm_config: Optional[dict] = None) -> Tuple[Optional[str], Optional[str], Optional[dict]]:
        if llm_config is None:
            llm_config = {}
        llm_engine = llm_config.get('engine', None)
        model = llm_config.get('model', None)
        model_config = llm_config.get('model_config', None)
        return llm_engine, model, model_config
        
    def setup_model(self, llm_engine: Optional[str] = None, model: Optional[str] = None, model_config: Optional[dict] = None) -> None:
        logger.info(f"Setting up LLM...")
        if llm_engine is None:
            llm_engine = 'openai'
        llm_cls = LLM_REGISTRY[llm_engine]
        self.llm = llm_cls(model, model_config)
        logger.info(f"LLM Engine: {llm_engine}")
        logger.info(f"Model ID/Path: {self.llm.model}")
        logger.info(f"Model Config: {model_config}")
        logger.info(f"LLM has been initialized.")
    
    def _search_from_arxiv(self, message: str, history: List[Tuple[str, str]], generation_config: Optional[Dict] = None, max_results: int = 5) -> Tuple[str, str]:
        response = self._chat(
            message=message,
            history=history,
            system_prompt=ARXIV_SEARCH_PROMPT,
            generation_config=generation_config,
            stream=False
        )
        papers = self.tool.call(response, max_results=max_results)
        return papers, response
        
        
    def _chat(self, message: str, history: List[Tuple[str, str]], system_prompt: Optional[str] = None, generation_config: Optional[Dict] = None, stream: bool = True) -> str:
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
    
    def chat(self, message: str, history_chat: List[Tuple[str, str]], history_search: List[Tuple[str, str]], generation_config: Optional[Dict] = None, max_results: int = 5, stream: bool = True) -> Tuple[str, str, str]:
        papers, paper_search_query = self._search_from_arxiv(message, history_search, generation_config, max_results)
        paper_cards = self._generate_paper_cards(papers)
        messaeg_for_llm = self._prepare_message_for_llm(message, papers)
        response = self._chat(
            message=messaeg_for_llm,
            history=history_chat,
            system_prompt=ARXIV_SYSTEM_PROMPT,
            generation_config=generation_config,
            stream=stream
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
            content += "作者：{authors}\n\n".format(authors=", ".join(paper["authors"]))
        
        message = ARXIV_CHAT_TEMPLATE.format(content=content, message=message)
        return message
        