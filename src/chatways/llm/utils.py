from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from chatways.registry import Registry


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
    engine: str = ""
    model: str = ""
    default_model: str = ""

    @abstractmethod
    def __init__(
        self, model: Optional[str] = None, model_config: Optional[Dict] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def invoke(self, messages: Any, generation_config: Optional[Dict] = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def invoke_stream(
        self, messages: Any, generation_config: Optional[Dict] = None
    ) -> Any:
        raise NotImplementedError
