from typing import Optional, Tuple, Any
from abc import ABC, abstractmethod
from chatways.llm.utils import LLM_REGISTRY
from chatways.log import logger


class BaseChatBot(ABC):
    def __init__(self, llm_config: Optional[dict] = None) -> None:
        llm_engine, model, model_config = self.parse_llm_config(llm_config)
        self.setup_model(llm_engine, model, model_config)

    def parse_llm_config(
        self, llm_config: Optional[dict] = None
    ) -> Tuple[Optional[str], Optional[str], Optional[dict]]:
        if llm_config is None:
            llm_config = {}
        llm_engine = llm_config.get("engine", None)
        model = llm_config.get("model", None)
        model_config = llm_config.get("model_config", None)
        return llm_engine, model, model_config

    def setup_model(
        self,
        llm_engine: Optional[str] = None,
        model: Optional[str] = None,
        model_config: Optional[dict] = None,
    ) -> None:
        logger.info("Setting up LLM...")
        if llm_engine is None:
            llm_engine = "openai"
        llm_cls = LLM_REGISTRY[llm_engine]
        self.llm = llm_cls(model, model_config)
        logger.info(f"LLM Engine: {llm_engine}")
        logger.info(f"Model ID/Path: {self.llm.model}")
        logger.info(f"Model Config: {model_config}")
        logger.info("LLM has been initialized.")

    @abstractmethod
    def chat(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
