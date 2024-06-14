from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod


TOOL_REGISTRY_MAP = {
    "arxiv": "ArxivTool",
}


def import_from_register(key):
    value = TOOL_REGISTRY_MAP[key]
    exec(f'from chatfactory.tool.{key} import {value}')


class ToolRegistry(dict):
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


TOOL_REGISTRY = ToolRegistry()


def register_tool(name):
    def decorator(cls):
        TOOL_REGISTRY[name] = cls
        return cls
    return decorator


class BaseTool(ABC):
    @abstractmethod
    def call(self, parameters_json: str, **kwargs) -> str:
        raise NotImplementedError
