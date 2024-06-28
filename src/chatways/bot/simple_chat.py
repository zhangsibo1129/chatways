from typing import Optional, Dict, List, Tuple, Any
from chatways.bot.utils import BaseChatBot


class SimpleChatBot(BaseChatBot):
    """A simple chat bot that uses a single LLM."""

    def chat(
        self,
        message: str,
        history: List[Tuple[str, str]],
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict] = None,
        stream: bool = True,
    ) -> Any:
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
