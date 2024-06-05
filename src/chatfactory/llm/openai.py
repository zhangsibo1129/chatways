
import os

from typing import Optional, Any
from openai import OpenAI

from chatfactory.llm.utils import BaseChatModel, register_llm


@register_llm("openai")
class OpenAIChatModel(BaseChatModel):
    """
    OpenAI Chat Completions
    """
    
    default_model: str = "gpt-4"
    model: str = ""
        
    def setup_model(self, model: Optional[str] = None, model_config: Optional[dict] = None) -> None:
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

    def invoke(self, messages: Any, generation_config: Optional[dict] = None) -> str:
        if generation_config is None:
            generation_config = {}

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **generation_config
        )
        return response.choices[0].message.content
