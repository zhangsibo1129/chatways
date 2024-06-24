import os
import sys
import json
import argparse
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(lib_dir)

from chatfactory.bot.chat import SimpleChatBot  # noqa: E402


CSS = """#chatbot1, #chatbot2 {
    height: 60vh !important;
    display: flex;
    flex-direction: column-reverse;
}
"""

HEADER = """# Chat Comparison

Chat Comparison lets you chat with two different language models simultaneously, so you can see how they answer the same question and identify the differences between them.
"""

OPENAI_PARAMEATERS = [
    ("temperature", 1.0, 0.0, 2.0, 0.01),
    ("top_p", 1.0, 0.0, 1.0, 0.01),
    ("frequency_penalty", 0.0, -2.0, 2.0, 0.01),
    ("presence_penalty", 0.0, -2.0, 2.0, 0.01),
]

HF_PARAMETERS = [
    ("temperature", 1.0, 0.0, 2.0, 0.01),
    ("top_k", 50, 0, 100, 1),
    ("top_p", 1.0, 0.0, 2.0, 0.01),
    ("max_new_tokens", 512, 0, 1024, 1),
]

FAKE_PARAMETERS = [
    ("temperature", 1.0, 0.0, 2.0, 0.01),
    ("top_k", 50, 0, 100, 1),
    ("top_p", 1.0, 0.0, 2.0, 0.01),
    ("max_new_tokens", 512, 0, 1024, 1),
]


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Chat Application")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        default="127.0.0.1",
        help="Default address is 127.0.0.1",
    )
    parser.add_argument(
        "-p", "--port", type=int, default=7860, help="Default port is 7860"
    )

    llm_group1 = parser.add_argument_group(
        "LLM Configuration 1", "Options for configuring the first LLM engine and model"
    )
    llm_group1.add_argument(
        "-le1",
        "--llm-engine1",
        type=str,
        default=None,
        help="The first LLM engine to use",
    )
    llm_group1.add_argument(
        "-lm1", "--llm-model1", type=str, default=None, help="The first LLM model path"
    )
    llm_group1.add_argument(
        "-lc1",
        "--llm-model-config1",
        type=str,
        default=None,
        help="The first LLM model configuration in JSON format",
    )

    llm_group2 = parser.add_argument_group(
        "LLM Configuration 2", "Options for configuring the second LLM engine and model"
    )
    llm_group2.add_argument(
        "-le2",
        "--llm-engine2",
        type=str,
        default=None,
        help="The second LLM engine to use",
    )
    llm_group2.add_argument(
        "-lm2", "--llm-model2", type=str, default=None, help="The second LLM model path"
    )
    llm_group2.add_argument(
        "-lc2",
        "--llm-model-config2",
        type=str,
        default=None,
        help="The second LLM model configuration in JSON format",
    )

    return parser.parse_args()


args = parse_args()

bot1 = SimpleChatBot(
    llm_config={
        "engine": args.llm_engine1,
        "model": args.llm_model1,
        "model_config": (
            json.loads(args.llm_model_config1) if args.llm_model_config1 else None
        ),
    }
)

bot2 = SimpleChatBot(
    llm_config={
        "engine": args.llm_engine2,
        "model": args.llm_model2,
        "model_config": (
            json.loads(args.llm_model_config2) if args.llm_model_config2 else None
        ),
    }
)


def get_generation_config1(components):
    if args.llm_engine1 == "openai" or args.llm_engine1 is None:
        parameters = OPENAI_PARAMEATERS
    elif args.llm_engine1 == "huggingface":
        parameters = HF_PARAMETERS
    elif args.llm_engine1 == "fake":
        parameters = FAKE_PARAMETERS

    parameter_components = components[: int(len(components) / 2)]
    availabel_components = components[int(len(components) / 2) :]
    generation_config = {}
    for parameter, parameter_component, availabel_component in zip(
        parameters, parameter_components, availabel_components
    ):
        if availabel_component:
            parameter_component = None
        generation_config.update({parameter[0]: parameter_component})
    return generation_config


def get_generation_config2(components):
    if args.llm_engine2 == "openai" or args.llm_engine2 is None:
        parameters = OPENAI_PARAMEATERS
    elif args.llm_engine2 == "huggingface":
        parameters = HF_PARAMETERS
    elif args.llm_engine2 == "fake":
        parameters = FAKE_PARAMETERS

    parameter_components = components[: int(len(components) / 2)]
    availabel_components = components[int(len(components) / 2) :]
    generation_config = {}
    for parameter, parameter_component, availabel_component in zip(
        parameters, parameter_components, availabel_components
    ):
        if availabel_component:
            parameter_component = None
        generation_config.update({parameter[0]: parameter_component})
    return generation_config


def respond1(message, history, system_prompt, stream, *components):
    generation_config = get_generation_config1(components)
    response = bot1.chat(
        message=message,
        history=history,
        system_prompt=system_prompt,
        generation_config=generation_config,
        stream=stream,
    )
    history.append([message, ""])
    if stream:
        for chunk in response:
            if chunk is not None:
                history[-1][1] += chunk
                yield "", history
    else:
        history[-1][1] = response
        yield "", history


def respond2(message, history, system_prompt, stream, *components):
    generation_config = get_generation_config2(components)
    response = bot2.chat(
        message=message,
        history=history,
        system_prompt=system_prompt,
        generation_config=generation_config,
        stream=stream,
    )
    history.append([message, ""])
    if stream:
        for chunk in response:
            if chunk is not None:
                history[-1][1] += chunk
                yield "", history
    else:
        history[-1][1] = response
        yield "", history


def clean_conversation():
    return "", [], []


def create_component(label, value, minimum, maximum, step):
    return gr.Slider(
        label=label,
        value=value,
        minimum=minimum,
        maximum=maximum,
        step=step,
        interactive=True,
    )


def enable_parameter_slider():
    return False


with gr.Blocks(css=CSS) as demo:
    gr.Markdown(HEADER)

    with gr.Row():
        system_prompt = gr.Textbox(
            placeholder="System Prompt", show_label=False, scale=9
        )
        stream_component = gr.Checkbox(
            value=True, label="Stream", interactive=True, scale=1
        )

    with gr.Row():
        chatbot1 = gr.Chatbot(
            elem_id="chatbot1", show_label=False, show_copy_button=True
        )
        chatbot2 = gr.Chatbot(
            elem_id="chatbot2", show_label=False, show_copy_button=True
        )

    with gr.Row():
        inputs = gr.Textbox(placeholder="Input", show_label=False, lines=2, scale=8)
        clean_btn = gr.Button(scale=1, value="Clean", variant="stop")
        send_btn = gr.Button(scale=1, value="Send", variant="primary")

    with gr.Row():
        with gr.Accordion("Parameters", open=False):
            if args.llm_engine1 == "openai" or args.llm_engine1 is None:
                parameters1 = OPENAI_PARAMEATERS
            elif args.llm_engine1 == "huggingface":
                parameters1 = HF_PARAMETERS
            elif args.llm_engine1 == "fake":
                parameters1 = FAKE_PARAMETERS

            availabel_components1 = []
            parameter_components1 = []
            index = 0
            while index < len(parameters1):
                with gr.Row():
                    with gr.Column():
                        parameter_components1.append(
                            create_component(*parameters1[index])
                        )
                        availabel_components1.append(
                            gr.Checkbox(label="Disable", value=True, interactive=True)
                        )
                        index += 1
                    if index < len(parameters1):
                        with gr.Column():
                            parameter_components1.append(
                                create_component(*parameters1[index])
                            )
                            availabel_components1.append(
                                gr.Checkbox(
                                    label="Disable", value=True, interactive=True
                                )
                            )
                            index += 1

        with gr.Accordion("Parameters", open=False):
            if args.llm_engine2 == "openai" or args.llm_engine2 is None:
                parameters2 = OPENAI_PARAMEATERS
            elif args.llm_engine2 == "huggingface":
                parameters2 = HF_PARAMETERS
            elif args.llm_engine2 == "fake":
                parameters2 = FAKE_PARAMETERS

            availabel_components2 = []
            parameter_components2 = []
            index = 0
            while index < len(parameters2):
                with gr.Row():
                    with gr.Column():
                        parameter_components2.append(
                            create_component(*parameters2[index])
                        )
                        availabel_components2.append(
                            gr.Checkbox(label="Disable", value=True, interactive=True)
                        )
                        index += 1
                    if index < len(parameters2):
                        with gr.Column():
                            parameter_components2.append(
                                create_component(*parameters2[index])
                            )
                            availabel_components2.append(
                                gr.Checkbox(
                                    label="Disable", value=True, interactive=True
                                )
                            )
                            index += 1

    inputs.submit(
        respond1,
        [
            inputs,
            chatbot1,
            system_prompt,
            stream_component,
            *(parameter_components1 + availabel_components1),
        ],
        [inputs, chatbot1],
    )
    inputs.submit(
        respond2,
        [
            inputs,
            chatbot2,
            system_prompt,
            stream_component,
            *(parameter_components2 + availabel_components2),
        ],
        [inputs, chatbot2],
    )
    send_btn.click(
        respond1,
        [
            inputs,
            chatbot1,
            system_prompt,
            stream_component,
            *(parameter_components1 + availabel_components1),
        ],
        [inputs, chatbot1],
    )
    send_btn.click(
        respond2,
        [
            inputs,
            chatbot2,
            system_prompt,
            stream_component,
            *(parameter_components2 + availabel_components2),
        ],
        [inputs, chatbot2],
    )
    clean_btn.click(clean_conversation, outputs=[inputs, chatbot1, chatbot2])

    for parameter_component, availabel_component in zip(
        parameter_components1, availabel_components1
    ):
        parameter_component.change(
            fn=enable_parameter_slider, outputs=availabel_component
        )

    for parameter_component, availabel_component in zip(
        parameter_components2, availabel_components2
    ):
        parameter_component.change(
            fn=enable_parameter_slider, outputs=availabel_component
        )

if __name__ == "__main__":
    demo.launch(server_name=args.address, server_port=args.port)
