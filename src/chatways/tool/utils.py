from abc import ABC, abstractmethod
from chatways.registry import Registry

TOOL_REGISTRY_MAP = {
    "arxiv": "ArxivTool",
}

TOOL_REGISTRY = Registry("tool", TOOL_REGISTRY_MAP)


def register_tool(name):
    def decorator(cls):
        TOOL_REGISTRY[name] = cls
        return cls

    return decorator


class BaseTool(ABC):
    @abstractmethod
    def call(self, parameters_json: str, **kwargs) -> str:
        raise NotImplementedError
