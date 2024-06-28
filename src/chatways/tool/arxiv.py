import re
import json
import arxiv
from typing import Optional, Tuple
from chatways.tool.utils import BaseTool, register_tool


@register_tool("arxiv")
class ArxivTool(BaseTool):
    name = "arxiv"
    description = "arXiv 论文搜索工具"

    @classmethod
    def construct_query(
        self, parameters_json: str
    ) -> Tuple[str, Optional[arxiv.SortCriterion]]:
        # in case of the """json {...}""" markdown code block style
        match = re.search(r"```json(.*?)```", parameters_json, re.DOTALL)
        if match:
            parameters_json = match.group(1).strip()
        try:
            parameters = json.loads(parameters_json)
        except json.JSONDecodeError:
            parameters = {}

        keywords = parameters.get("research_field", [])
        if not isinstance(keywords, list):
            keywords = []
        authors = parameters.get("authors", [])
        if not isinstance(authors, list):
            authors = []
        order = parameters.get("search_order", "")
        if not isinstance(order, str):
            order = ""
        # Relevance performs best
        order = arxiv.SortCriterion.Relevance
        # if order == "Latest":
        #     order = arxiv.SortCriterion.SubmittedDate
        # else:
        #     order = arxiv.SortCriterion.Relevance

        # no avaliable parameters
        if (not keywords) and (not authors):
            return "", None
        # refer to arXiv api documentation
        query = ""
        if keywords:
            query += "all:"
            for keyword in keywords:
                query += keyword + " "
        if authors:
            if keywords:
                query += "AND "
            query += "au:"
            for author in authors:
                query += author + " "
        return query, order

    def call(self, parameters_json: str, **kwargs) -> str:
        query, order = self.construct_query(parameters_json)
        if not query:
            return ""

        client = arxiv.Client()
        max_results = kwargs.get("max_results", 5)
        search = arxiv.Search(query=query, max_results=max_results, sort_by=order)

        papers = []
        for result in client.results(search):
            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            }
            papers.append(paper)
        return json.dumps(papers)
