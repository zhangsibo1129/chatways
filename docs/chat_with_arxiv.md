# Chat with arXiv

Using LLM to make finding academic papers on arXiv more natural and insightful

## Interface

![chat_with_arxiv](figures/chat_with_arxiv.png)

## Command

General Form

```bash
chatways arxiv [options]
```

- **Case 1** Use Default Parameters

```bash
chatways arxiv
```

- **Case 2** Config with Full Parameters

```bash
chatways arxiv \
    --llm-engine openai \
    --llm-model gpt-3.5-turbo \
    --llm-model-config '{"api_key":"openai_api_key","base_url":"openai_base_url"}'
```

- **Case 3** Set Partial Parameters with Abbreviations

```bash
chatways arxiv \
    -le huggingface \
    -lc '{"torch_dtype":"auto","device_map":"auto"}'
```

## Configuration

- **Address**
  - **Full Name**: `--address`
  - **Abbreviation**: `-a`
  - **Default Value**: `"127.0.0.1"`
  - **Description**: Address to which the application binds

- **Port**
  - **Full Name**: `--port`
  - **Abbreviation**: `-p`
  - **Default Value**: `7860`
  - **Description**: Port number to which the application binds

- **LLM Engine**
  - **Full Name**: `--llm-engine`
  - **Abbreviation**: `-le`
  - **Default Value**: `None`
  - **Description**: LLM engine

- **LLM Model**
  - **Full Name**: `--llm-model`
  - **Abbreviation**: `-lm`
  - **Default Value**: `None`
  - **Description**: LLM model path or name

- **LLM Model Config**
  - **Full Name**: `--llm-model-config`
  - **Abbreviation**: `-lc`
  - **Default Value**: `None`
  - **Description**: JSON configuration for the LLM
