# Chat Comparison

同时与两个 LLM 对话，针对同一输入，比较两个 LLM 的输出

## 应用界面

![chat_comparison](figures/chat_comparison.png)

## 启动命令

一般形式

```bash
chatways comparison [options]
```

- **样例1** 使用默认参数

```bash
chatways comparison
```

- **样例2** 设置完整参数

```bash
chatways comparison \
    --llm-engine1 openai \
    --llm-model1 gpt-3.5-turbo \
    --llm-model-config1 '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
    --llm-engine2 huggingface \
    --llm-model2 Qwen/Qwen1.5-4B-Chat \
    --llm-model-config2 '{"torch_dtype":"auto","device_map":"auto"}'
```

- **样例3** 用简称指定部分参数

```bash
chatways comparison \
    --le1 openai \
    --le2 huggingface \
    --lc2 '{"torch_dtype":"auto","device_map":"auto"}'
```

## 配置参数


- **Address**
  - **全称**: `--address`
  - **简称**: `-a`
  - **默认值**: `"127.0.0.1"`
  - **描述**: 指定应用程序绑定的地址。默认值为 `127.0.0.1`。

- **Port**
  - **全称**: `--port`
  - **简称**: `-p`
  - **默认值**: `7860`
  - **描述**: 指定应用程序绑定的端口号。默认值为 `7860`。

- **LLM Engine 1**
  - **全称**: `--llm-engine1`
  - **简称**: `-le1`
  - **默认值**: `None`
  - **描述**: 指定第一个LLM引擎。

- **LLM Model 1**
  - **全称**: `--llm-model1`
  - **简称**: `-lm1`
  - **默认值**: `None`
  - **描述**: 指定第一个LLM模型路径。

- **LLM Model Config 1**
  - **全称**: `--llm-model-config1`
  - **简称**: `-lc1`
  - **默认值**: `None`
  - **描述**: 指定第一个LLM模型的JSON格式配置文件。

- **LLM Engine 2**
  - **全称**: `--llm-engine2`
  - **简称**: `-le2`
  - **默认值**: `None`
  - **描述**: 指定第二个LLM引擎。

- **LLM Model 2**
  - **全称**: `--llm-model2`
  - **简称**: `-lm2`
  - **默认值**: `None`
  - **描述**: 指定第二个LLM模型路径。

- **LLM Model Config 2**
  - **全称**: `--llm-model-config2`
  - **简称**: `-lc2`
  - **默认值**: `None`
  - **描述**: 指定第二个LLM模型的JSON格式配置文件。
