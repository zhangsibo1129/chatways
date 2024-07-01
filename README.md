# Chatways 

<p align="center">
    <b>English</b> |
    <a href="https://github.com/zhangsibo1129/chatways/blob/main/README_zh.md">中文</a>
<p>

Chatways provides a simple way to build chat applications with LLMs, offering templates, interfaces, and support for multiple LLM backends.

## Features

- [Template-driven](#templates) application creation for non-coders, enabling app launching with a single command.
- Simplified API interfaces for developers, eliminating complex development workflows.
- Integration with multiple LLM backends, including OpenAI and Hugging Face.

## Quickstart

1. Install from PyPI:

    ```bash
    pip install chatways
    ```

    or from source:

    ```bash
    git clone https://github.com/zhangsibo1129/chatways.git
    cd chatways
    pip install -e .
    ```

2. launch the chat application using `chatways` command:

    ```bash
    chatways simple --llm-engine fake --port 7860
    ```

    - `simple` starts a basic chat application.
    - `--llm-engine fake` uses a simulated LLM engine, requiring no local GPU or remote API.
    - `--port 7860` sets the port address.
    For detailed parameter information, refer to the [templates](#templates).

3. Open your browser and visit `http://localhost:7860` to interact with the chat application.

    ![chatways-demo](docs/figures/simple_chat.png)

## How to use

### Launch Templates with CLI Command

Chatways offers a range of ready-to-use templates. Templates applications can be quickly launched with a `chatways` command, and LLM backends can be easily swapped, making it ideal for no-code builders. The command structure is as follows:

```bash
chatways [template] [options]
```

- template: Specifies the type of application (e.g., simple, comparison, arxiv).
- options: Configuration parameters:
  - --llm-engine (-le): LLM engine to use (e.g., openai, huggingface).
  - --llm-model (-lm): LLM model to use (e.g., llama).
  - --llm-config (-lc): Additional configuration in JSON format (e.g., {"device_map":"auto"}).

Here are some examples:

- launch a simple chat application with openai backend

    ```bash
    export OPENAI_API_KEY="openai_api_key"
    export OPENAI_BASE_URL="openai_base_url"
    chatways simple -le openai -lm gpt-3.5-turbo
    ```

    or

    ```bash
    chatways simple \
        --llm-engine openai \
        --llm-model gpt-3.5-turbo \
        --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
    ```

- launch a Chat with arXiv application with huggingface backend:

    ```bash
    chatways arxiv \
        --llm-engine huggingface \
        --llm-model Qwen/Qwen1.5-4B-Chat \
        --llm-model-config '{"torch_dtype":"auto","device_map":"auto"}'
    ```

### Quick Customization with Templates

The `src/chatways/template` directory contains templates built with the `chatways` library. Each application template is an independently runnable Gradio app. Users can quickly customize these templates, making it much easier than developing an application from scratch.

### Integration with Bot Module

The `bot` module provides a highly abstract interface designed to simplify integration. This module allows developers to seamlessly integrate LLM into their workflow.

1. Create a chatbot instance

    ```python
    >>> from chatways import SimpleChatBot

    >>> bot = SimpleChatBot(
    ...     llm_engine = "huggingface",
    ...     model = "Qwen/Qwen1.5-4B-Chat",
    ...     model_config = {
    ...         "torch_dtype":"auto",
    ...         "device_map":"auto"
    ...     }
    ... )
    ```

2. Chat with the bot

    ```python
    >>> history = []
    >>> query = "Say three positive words"
    >>> response = bot.chat(query, history=history, stream=False)
    >>> print(response)
    1. hope
    2. confidence 
    3. inspiration
    ```

    ```python
    >>> history.append([query, response]) # Maintain Conversation History
    >>> query = "Please use the second one in a sentence"
    >>> response = bot.chat(query, history=history, stream=False)
    >>> print(response)
    The confidence he had in himself gave him strength to face any challenge that came his way.
    ```

## Templates

Currently, Chatways provides the following application templates:

| Category | Feature | Command |
|:----------:|----------|----------|
| [**Chat**](docs/simple_chat.md) | Simple chat application that enables multi-round conversations with LLM | `chatways simple [options]` |
| [**Chat Comparison**](docs/chat_comparison.md) | Chat with 2 LLMs simultaneously and compare their results | `chatways comparison [options]` |
| [**Chat with arXiv**](docs/chat_with_arxiv.md) | Using LLM to make finding academic papers on arXiv more natural and insightful | `chatways arxiv [options]` |

## Contributing

As this project is in its early stages, all kinds of contributions are welcome, whether it's reporting issues, suggesting new features, or submitting pull requests.

## License

This project is licensed under the MIT License.
