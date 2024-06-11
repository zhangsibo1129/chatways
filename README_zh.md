# chatfactory

<p align="center">
    <a href="https://github.com/zhangsibo1129/chatfactory/blob/main/README.md">English</a> |
    <b>中文</b>
<p>

Chatfactory 用于快速构建基于 LLM 的聊天应用，它提供了多种拿来即用的应用模板，也提供抽象接口进行自定义开发，并支持多种 LLM 后端

## 特点

- [**模板化应用创建**](#应用模板)，对于无代码应用开发者，只需一条命令即可快速创建应用
- **高度抽象的 API 接口**，为代码开发者提供高度集成的模块，简化代码开发
- **多种 LLM 后端支持**，包括 OpenAI 和 Huggingface 等

## 安装

1. 克隆仓库：

    ```bash
    git clone https://github.com/zhangsibo1129/chatfactory.git
    ```

2. 安装依赖：

    ```bash
    cd chatfactory
    pip install -r requirements.txt
    ```

## 快速入门

在没有本地 GPU 算力和远端 API 资源的情况下，你可以通过一行命令快速启动一个模拟的聊天应用

1. 启动一个简单聊天应用，采用模拟 LLM 后端：

    ```bash
    python src/chatfactory/app/simple_chat.py --llm-engine fake --port 7860
    ```

2. 打开浏览器访问 `http://localhost:7860`，即可看到应用界面

    ![chatfactory-demo](docs/figures/simple_chat.png)

## 使用教程

### 用模板创建应用

Chatfactory 提供了多种模应用模板，以 Simple Chat 为例，你可以通过以下命令快速启动：

- 采用 openai 后端，通过环境变量配置 `openai_api_key` 等信息:

    ```bash
    export OPENAI_API_KEY="openai_api_key"
    export OPENAI_BASE_URL="openai_base_url"
    python src/chatfactory/app/simple_chat.py --llm-engine openai
    ```

    或者，将 `openai_api_key` 作为模型参数传入：

    ```bash
    python src/chatfactory/app/simple_chat.py \
        --llm-engine openai \
        --llm-model gpt-3.5-turbo \
        --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
    ```

- 采用 Huggingface 后端：

    ```bash
    python src/chatfactory/app/simple_chat.py \
        --llm-engine huggingface \
        --llm-model Qwen/Qwen1.5-4B-Chat \
        --llm-model-config '{"torch_dtype":"auto","device_map":"auto"}'
    ```

### 使用 bot 模块

Chatfactory 提供了高度抽象的 `bot` 模块，该模块允许开发者调用简单接口，实现与自身业务的无缝集成。一般步骤如下：

1. 模型配置

    ```python
    import os
    os.environ['OPENAI_API_KEY'] = "openai_api_key"
    os.environ['OPENAI_BASE_URL'] = "openai_base_url"

    llm_config = dict(
        engine = "huggingface",
        model = "gpt-3.5-turbo-16k-0613",
    )
    ```

2. 创建 bot 实例

    ```python
    from chatfactory.bot.chat import SimpleChatBot

    bot = SimpleChatBot(llm_config)
    ```

3. 与 bot 进行交互

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

## 应用模板

目前 Chatfactory 提供了以下应用模板：

| Name | 功能 | 启动命令 | 参数（可选）|
|:----------:|----------|----------|----------|
| [**Chat**](docs/simple_chat.md) | 简单的聊天应用，实现与 LLM 的多轮对话 | python simple_chat.py | `--address`<br>`--port`<br>`--llm-engine` <br>`--llm-model` <br>`--llm-model-config`|
| [**Chat Comparison**](docs/chat_comparison.md) | 同时与2个LLM进行对话，对二者的结果进行对照 | python chat_comparison.py | `--address`<br>`--port`<br>`--llm-engine1` <br>`--llm-model1` <br>`--llm-model-config1` <br>`--llm-engine2` <br>`--llm-model2` <br>`--llm-model-config2`|

## 贡献

Chatfactory 项目目前在初期阶段，欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 建议新功能
- 提交 PR

## License

This project is licensed under the MIT License.
