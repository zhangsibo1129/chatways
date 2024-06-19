# chatfactory

<p align="center">
    <b>English</b> |
    <a href="https://github.com/zhangsibo1129/chatfactory/blob/main/README_zh.md">中文</a>
<p>

Chatfactory provides an easy way to build chat applications with LLMs, offering templates, interfaces, and support for multiple llm backends.

## Features

- [Template-driven](#application-templates) application creation for non-coders, enabling app development with just one command.
- Simplified API interface for developers, eliminating complex development workflows.
- Integration with multiple LLM backends, including OpenAI and Hugging Face.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/zhangsibo1129/chatfactory.git
    ```

2. Install the required dependencies:

    ```bash
    cd chatfactory
    pip install -r requirements.txt
    ```

## Quickstart

You can quickly start a chat application with the following one-line command, without local GPU or remote API resources.

1. launch the chat application:

    ```bash
    python src/chatfactory/app/simple_chat.py --llm-engine fake --port 7860
    ```

2. Open your browser and visit `http://localhost:7860` to interact with the chat application.

    ![chatfactory-demo](docs/figures/simple_chat.png)

## How to use

### Launch a template application

- launch a chat application with openai backend:

    ```bash
    export OPENAI_API_KEY="openai_api_key"
    export OPENAI_BASE_URL="openai_base_url"
    python src/chatfactory/app/simple_chat.py --llm-engine openai
    ```

    or

    ```bash
    python src/chatfactory/app/simple_chat.py \
        --llm-engine openai \
        --llm-model gpt-3.5-turbo \
        --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
    ```

- launch a chat application with huggingface backend:

    ```bash
    python src/chatfactory/app/simple_chat.py \
        --llm-engine huggingface \
        --llm-model Qwen/Qwen1.5-4B-Chat \
        --llm-model-config '{"torch_dtype":"auto","device_map":"auto"}'
    ```

### Use bot moudle

The `bot` module provides a highly abstract interface designed to simplify integration. This module allows developers to seamlessly integrate llm into their workflow.

1. Model Configuration

    ```python
    import os
    os.environ['OPENAI_API_KEY'] = "openai_api_key"
    os.environ['OPENAI_BASE_URL'] = "openai_base_url"

    llm_config = dict(
        engine = "huggingface",
        model = "gpt-3.5-turbo-16k-0613",
    )
    ```

2. Create a chatbot instance

    ```python
    from chatfactory.bot.chat import SimpleChatBot

    bot = SimpleChatBot(llm_config)
    ```

3. Chat with the bot

    ```python
    history = []
    query = "Say three positive words"
    response = bot.chat(query, history=history, stream=False)
    print(response)
    # Output:
    # Love, happiness, success

    history.append([query, response]) # Maintain Conversation History

    query = "Please use the second one in a sentence"
    response = bot.chat(query, history=history, stream=False)
    print(response)
    # Output:
    # Her infectious laughter filled the room with happiness.
    ```

## Application Templates

Currently, Chatfactory provides the following application templates:

| Name | Function | Launch Command | Parameters (Optional) |
|:----------:|----------|----------|----------|
| [**Chat**](docs/simple_chat.md) | Simple chat application that enables multi-round conversations with LLM | python simple_chat.py | `--address`<br>`--port`<br>`--llm-engine` <br>`--llm-model` <br>`--llm-model-config`|
| [**Chat Comparison**](docs/chat_comparison.md) | Chat with 2 LLMs simultaneously and compare their results | python chat_comparison.py | `--address`<br>`--port`<br>`--llm-engine1` <br>`--llm-model1` <br>`--llm-model-config1` <br>`--llm-engine2` <br>`--llm-model2` <br>`--llm-model-config2`|
| [**Chat with arXiv**](docs/chat_with_arxiv.md) | Using LLM to make finding academic papers on arXiv more natural and insightful | python chat_with_arxiv.py | `--address`<br>`--port`<br>`--llm-engine` <br>`--llm-model` <br>`--llm-model-config`|

## Contributing

As this project is in its early stages, all kinds of contributions are welcome, whether it's reporting issues, suggesting new features, or submitting pull requests.

## License

This project is licensed under the MIT License.
