import os
import argparse


def generate_command(args, filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "template", filename)
    arguments = " "
    for key, value in vars(args).items():
        if not value:
            continue
        if key != "command" and key != "func":
            key = key.replace("_", "-")
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                value = f"'{value}'"
            arguments += f"--{key} {value} "
    command = "python " + file_path + arguments
    return command


def run_simple_template(args):
    filename = "simple_chat.py"
    command = generate_command(args, filename)
    os.system(command)


def run_comparison_template(args):
    filename = "chat_comparison.py"
    command = generate_command(args, filename)
    os.system(command)


def run_arxiv_template(args):
    filename = "chat_with_arxiv.py"
    command = generate_command(args, filename)
    os.system(command)


def add_simple_chat_subparser(subparsers):
    simple_chat_parser = argparse.ArgumentParser(
        description="Simple Chat Application", add_help=False
    )
    simple_chat_parser.add_argument(
        "-a",
        "--address",
        type=str,
        default="127.0.0.1",
        help="Default address is 127.0.0.1",
    )
    simple_chat_parser.add_argument(
        "-p", "--port", type=int, default=7860, help="Default port is 7860"
    )
    simple_chat_parser.add_argument(
        "-le", "--llm-engine", type=str, default=None, help="The LLM engine to use"
    )
    simple_chat_parser.add_argument(
        "-lm", "--llm-model", type=str, default=None, help="The LLM model path"
    )
    simple_chat_parser.add_argument(
        "-lc",
        "--llm-model-config",
        type=str,
        default=None,
        help="The LLM model configuration in JSON format",
    )
    _parser = subparsers.add_parser("simple", parents=[simple_chat_parser])
    _parser.set_defaults(func=run_simple_template)


def add_chat_comparison_subparser(subparsers):
    chat_comparison_parser = argparse.ArgumentParser(
        description="Simple Chat Application", add_help=False
    )
    chat_comparison_parser.add_argument(
        "-a",
        "--address",
        type=str,
        default="127.0.0.1",
        help="Default address is 127.0.0.1",
    )
    chat_comparison_parser.add_argument(
        "-p", "--port", type=int, default=7860, help="Default port is 7860"
    )

    llm_group1 = chat_comparison_parser.add_argument_group(
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

    llm_group2 = chat_comparison_parser.add_argument_group(
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
    _parser = subparsers.add_parser("comparison", parents=[chat_comparison_parser])
    _parser.set_defaults(func=run_comparison_template)


def add_chat_with_arxiv_subparser(subparsers):
    chat_with_arxiv_parser = argparse.ArgumentParser(
        description="Simple Chat Application", add_help=False
    )
    chat_with_arxiv_parser.add_argument(
        "-a",
        "--address",
        type=str,
        default="127.0.0.1",
        help="Default address is 127.0.0.1",
    )
    chat_with_arxiv_parser.add_argument(
        "-p", "--port", type=int, default=7860, help="Default port is 7860"
    )
    chat_with_arxiv_parser.add_argument(
        "-le", "--llm-engine", type=str, default=None, help="The LLM engine to use"
    )
    chat_with_arxiv_parser.add_argument(
        "-lm", "--llm-model", type=str, default=None, help="The LLM model path"
    )
    chat_with_arxiv_parser.add_argument(
        "-lc",
        "--llm-model-config",
        type=str,
        default=None,
        help="The LLM model configuration in JSON format",
    )
    _parser = subparsers.add_parser("arxiv", parents=[chat_with_arxiv_parser])
    _parser.set_defaults(func=run_arxiv_template)


def parse_args():
    parser = argparse.ArgumentParser(description="Chat Application CLI")
    subparsers = parser.add_subparsers(dest="command")
    add_simple_chat_subparser(subparsers)
    add_chat_comparison_subparser(subparsers)
    add_chat_with_arxiv_subparser(subparsers)
    return parser.parse_args()


def main():
    args = parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No command provided. Use --help for more information.")


if __name__ == "__main__":
    main()
