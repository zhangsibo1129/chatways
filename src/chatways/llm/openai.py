import os

from typing import Optional, Generator, Any
from openai import OpenAI

from chatways.llm.utils import BaseChatModel, register_llm


@register_llm("openai")
class OpenAIChatModel(BaseChatModel):
    """
    OpenAI Chat Completions
    """

    engine: str = "openai"
    model: str = ""
    default_model: str = "gpt-3.5-turbo"

    def __init__(
        self, model: Optional[str] = None, model_config: Optional[dict] = None
    ) -> None:
        if model is None:
            self.model = self.default_model
        else:
            self.model = model
        if model_config is None:
            model_config = {}
        api_key = model_config.get("api_key", None)
        base_url = model_config.get("base_url", None)
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY", None)
        if base_url is None:
            base_url = os.getenv("OPENAI_BASE_URL", None)
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def _generator_filter(self, response):
        for chunk in response:
            if len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content

    def invoke(self, messages: Any, generation_config: Optional[dict] = None) -> str:
        if generation_config is None:
            generation_config = {}

        generation_config.update({"stream": False})
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, **generation_config
        )
        response = response.choices[0].message.content
        return response

    def invoke_stream(
        self, messages: Any, generation_config: Optional[dict] = None
    ) -> Generator:
        if generation_config is None:
            generation_config = {}

        generation_config.update({"stream": True})
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, **generation_config
        )
        response = self._generator_filter(response)
        return response
