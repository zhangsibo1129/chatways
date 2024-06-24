from typing import Optional, Dict, List, Tuple
from chatfactory.llm.utils import LLM_REGISTRY
from chatfactory.log import logger


class SimpleChatBot:
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
        logger.info(f"Setting up LLM...")
        if llm_engine is None:
            llm_engine = "openai"
        llm_cls = LLM_REGISTRY[llm_engine]
        self.llm = llm_cls(model, model_config)
        logger.info(f"LLM Engine: {llm_engine}")
        logger.info(f"Model ID/Path: {self.llm.model}")
        logger.info(f"Model Config: {model_config}")
        logger.info(f"LLM has been initialized.")

    def chat(
        self,
        message: str,
        history: List[Tuple[str, str]],
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict] = None,
        stream: bool = True,
    ) -> str:
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
