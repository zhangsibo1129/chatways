from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod
from chatfactory.registry import Registry


LLM_REGISTRY_MAP = {
    "openai": "OpenAIChatModel",
    "huggingface": "HFChatModel",
    "fake": "FakeChatModel",
}

LLM_REGISTRY = Registry("llm", LLM_REGISTRY_MAP)


def register_llm(name):
    def decorator(cls):
        LLM_REGISTRY[name] = cls
        return cls

    return decorator


class BaseChatModel(ABC):
    def __init__(
        self, model: Optional[str] = None, model_config: Optional[Dict] = None
    ) -> None:
        self.setup_model(model, model_config)

    @abstractmethod
    def setup_model(
        self, model: Optional[str] = None, model_config: Optional[Dict] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def invoke(
        self, messages: List[Dict], generation_config: Optional[Dict] = None
    ) -> Any:
        raise NotImplementedError
