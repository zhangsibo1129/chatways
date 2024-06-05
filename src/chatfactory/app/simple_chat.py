import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(lib_dir)

import json
import argparse
import gradio as gr

from chatfactory.bot.chat import SimpleChatBot


CSS = """#chatbot {
    height: 60vh !important;
    display: flex;
    flex-direction: column-reverse;
}
"""

HEADER = """# Simple Chat Application

This is a simple chat application that uses a language model to generate responses.
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Simple Chat Application")
    parser.add_argument("-le", "--llm-engine", type=str, default=None, help="The LLM engine to use")
    parser.add_argument("-lm", "--llm-model", type=str, default=None, help="The LLM model path")
    parser.add_argument("-lc", "--llm-model-config", type=str, default=None, help="The LLM model configuration in JSON format")
    return parser.parse_args()

args = parse_args()

bot = SimpleChatBot(
    llm_config={
        "engine": args.llm_engine,
        "model": args.llm_model,
        "model_config": json.loads(args.llm_model_config) if args.llm_model_config else None
    }
)

def respond(message, history, system_prompt, stream=True):
    history.append((message, ""))
    response = bot.chat(
        message=message,
        history=history,
        system_prompt=system_prompt,
        generation_config=None,
        stream=stream
    )
    if stream:
        reply = ""
        for chunk in response:
            if chunk is not None:
                reply += chunk
                history[-1] = (history[-1][0], reply)
                yield "", history
    else:
        history[-1] = (history[-1][0], response)
        yield "", history

with gr.Blocks(css=CSS) as demo:
    gr.Markdown(HEADER)

    system_prompt = gr.Textbox(placeholder= "System Prompt", show_label=False)
    chatbot = gr.Chatbot(elem_id="chatbot", show_label=False)
    
    with gr.Row():
        inputs = gr.Textbox(placeholder= "Input", show_label=False, lines=2, scale=9)
        b1 = gr.Button(scale=1, value="Send", variant="primary")
    
    with gr.Accordion("Parameters", open=False):
        with gr.Row():
            top_p = gr.Slider( minimum=-0, maximum=1.0, value=1.0, step=0.05, interactive=True, label="Top-p (nucleus sampling)",)
            temperature = gr.Slider( minimum=-0, maximum=5.0, value=1.0, step=0.1, interactive=True, label="Temperature",)
        with gr.Row():
            top_k = gr.Slider( minimum=1, maximum=50, value=4, step=1, interactive=True, label="Top-k",)
            repetition_penalty = gr.Slider( minimum=0.1, maximum=3.0, value=1.03, step=0.01, interactive=True, label="Repetition Penalty", )
    
    inputs.submit(respond, [inputs, chatbot, system_prompt], [inputs, chatbot])
 
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
