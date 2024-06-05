from typing import Optional, Dict, List
from abc import ABC, abstractmethod


LLM_REGISTRY_MAP = {
    "openai": "OpenAIChatModel",
    "huggingface": "HFChatModel",
}


def import_from_register(key):
    value = LLM_REGISTRY_MAP[key]
    exec(f'from chatfactory.llm.{key} import {value}')


class LLMRegistry(dict):
    def _import_key(self, key):
        try:
            import_from_register(key)
        except Exception as e:
            print(f'import {key} failed, details: {e}')

    def __getitem__(self, key):
        if key not in self.keys():
            self._import_key(key)
        return super().__getitem__(key)

    def __contains__(self, key):
        self._import_key(key)
        return super().__contains__(key)


LLM_REGISTRY = LLMRegistry()


def register_llm(name):
    def decorator(cls):
        LLM_REGISTRY[name] = cls
        return cls
    return decorator


class BaseChatModel(ABC):
    def __init__(self, model: Optional[str] = None, model_config: Optional[Dict] = None) -> None:
        self.setup_model(model, model_config)
    
    @abstractmethod
    def setup_model(self, model: Optional[str] = None, model_config: Optional[Dict] = None) -> None:
        raise NotImplementedError
        
    @abstractmethod
    def invoke(self, messages: List[Dict], generation_config: Optional[Dict] = None) -> str:
        raise NotImplementedError
