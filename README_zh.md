# Chatways

<p align="center">
    <a href="https://github.com/zhangsibo1129/chatways/blob/main/README.md">English</a> |
    <b>中文</b>
<p>

Chatways 用于快速构建基于 LLM 的聊天应用，它提供了多种拿来即用的应用模板，也提供抽象接口进行自定义开发，并支持多种 LLM 后端

## 特点

- [**模板化应用创建**](#应用模板)，对于无代码应用开发者，只需一条命令即可快速启动应用
- **易用的 API 接口**，为代码开发者提供高度集成的模块，简化代码开发
- **多种 LLM 后端支持**，包括 OpenAI 和 Huggingface 等

## 快速入门

1. 从 PyPI 仓库安装：

   ```bash
    pip install chatways
    ```

    或者从源码安装：

    ```bash
    git clone https://github.com/zhangsibo1129/chatways.git
    cd chatways
    pip install -e .
    ```

2. 用 `chatways` 命令启动一个聊天应用

    ```bash
    chatways simple --llm-engine fake --port 7860
    ```

    - `simple` 表示启动一个过简单的聊天应用
    - `--llm-engine fake` 表示采用虚拟的 LLM 后端，可以在没有本地 GPU 或者远端 API 服务情况下，进行快速验证
    - `--port 7860` 设置端口地址
    详细的参数配置请参考[应用模板](#应用模板).

3. 打开浏览器访问 `http://localhost:7860`，即可看到应用界面

    ![chatways-demo](docs/figures/simple_chat.png)

## 使用教程

### 用 CLI 启动模板

Chatways 内置了多种拿来即用的应用模板，使用 `chatways` 命令即可快速启动模板应用，并轻松切换 LLM 后端，非常适合无代码应用构建者。`chatways` 命令结构如下：

```bash
chatways [template] [options]
```

- template: 指定应用的类型（例如：simple, comparison, arxiv）
- options: 配置参数
  - --llm-engine (-le): LLM 引擎 （例如：openai, huggingface）
  - --llm-model (-lm): LLM 模型 （例如：llama）
  - --llm-config (-lc): JSON 格式模型配置参数(例如：{"device_map":"auto"})

以下是一些样例：

- 启动一个简单的聊天应用，使用 OpenAI 后端

    ```bash
    export OPENAI_API_KEY="openai_api_key"
    export OPENAI_BASE_URL="openai_base_url"
    chatways simple -le openai -lm gpt-3.5-turbo
    ```

    或者

    ```bash
    chatways simple \
        --llm-engine openai \
        --llm-model gpt-3.5-turbo \
        --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
    ```

- 启动一个 Chat with arXiv 应用，使用 Huggingface 后端

    ```bash
    chatways arxiv \
        --llm-engine huggingface \
        --llm-model Qwen/Qwen1.5-4B-Chat \
        --llm-model-config '{"torch_dtype":"auto","device_map":"auto"}'
    ```

### 用模板快速定制应用

在 `src/chatways/template` 文件夹提供了多种应用模板，这些模板都是基于 `chatways` 库构建的，每个应用模板都是一个独立可运行的 Gradio 应用。用户可以基于这些模板快速定制自己的应用，而无需从头开始开发。


### 用 Bot 模块实现集成

Chatways 提供了高度抽象的 `bot` 模块，该模块使开发者通过简单接口调用，实现与自身业务的无缝集成。一般步骤如下：

1. 创建 bot 实例

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

2. 与 bot 进行交互

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

## 应用模板

目前 Chatways 提供了以下应用模板：

| 类型 | 功能 | 启动命令 |
|:----------:|----------|----------|
| [**Chat**](docs/simple_chat.md) | 简单的聊天应用，实现与 LLM 的多轮对话 | `chatways simple [options]` |
| [**Chat Comparison**](docs/chat_comparison.md) | 同时与2个LLM进行对话，对二者的结果进行对照 | `chatways comparison [options]` |
| [**Chat with arXiv**](docs/chat_with_arxiv.md) | 在 arXiv 上更加智能、人性化地搜索学术论文 | `chatways arxiv [options]` |

## 贡献

Chatways 项目目前在初期阶段，欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 建议新功能
- 提交 PR

## License

This project is licensed under the MIT License.
