from setuptools import setup, find_packages

setup(
    name="chatways",
    version="0.1.0-dev0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "gradio",
        "transformers",
        "openai",
        "sentencepiece",
        "protobuf",
        "accelerate",
    ],
    entry_points={
        "console_scripts": [
            "chatways=chatways.cli:main",
        ],
    },
    author="Sibo Zhang",
    author_email="zhangsibo1129@gmail.com",
    description="A command line tool for chatways",
    url="https://github.com/zhangsibo1129/chatways",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
