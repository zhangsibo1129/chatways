# Simple Chat

简单的聊天应用，实现与 LLM 的多轮对话。

## 应用界面

![simple_chat](figures/simple_chat.png)

## 启动命令

一般形式

```bash
chatways simple [options]
```

- **样例1** 使用默认参数

```bash
chatways simple
```

- **样例2** 设置完整参数

```bash
chatways simple \
    --llm-engine openai \
    --llm-model gpt-3.5-turbo \
    --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
```

- **样例3** 用简称指定部分参数

```bash
chatways simple \
    -le huggingface \
    -lc '{"torch_dtype":"auto","device_map":"auto"}'
```

## 配置参数

- **Address**
  - **全称**: `--address`
  - **简称**: `-a`
  - **默认值**: `"127.0.0.1"`
  - **描述**: 指定应用程序绑定的地址

- **Port**
  - **全称**: `--port`
  - **简称**: `-p`
  - **默认值**: `7860`
  - **描述**: 指定应用程序绑定的端口号

- **LLM Engine**
  - **全称**: `--llm-engine`
  - **简称**: `-le`
  - **默认值**: `None`
  - **描述**: 指定 LLM 引擎

- **LLM Model**
  - **全称**: `--llm-model`
  - **简称**: `-lm`
  - **默认值**: `None`
  - **描述**: 指定第 LLM 路径或名称

- **LLM Model Config**
  - **全称**: `--llm-model-config`
  - **简称**: `-lc`
  - **默认值**: `None`
  - **描述**: 指定 LLM 的 JSON 格式配置
