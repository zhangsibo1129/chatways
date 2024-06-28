from setuptools import setup, find_packages

setup(
    name='chatf',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages("src"),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'chatf=chatfactory.cli:main',
        ],
    },
    author='Your Name',
    author_email='your_email@example.com',
    description='A command line tool for chat project',
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/chat',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
