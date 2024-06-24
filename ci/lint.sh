#!/usr/bin/bash

# Install dependencies
pip install black ruff

python -c 'import black' &> /dev/null
if [ $? -ne 0 ]; then
    echo "The 'black' python module was not found. Please try 'pip install black'."
    exit
fi

# Check installation.
if ! hash ruff 2> /dev/null; then
    echo "The 'ruff' command was not found. Please try 'pip install ruff'."
    return
fi

python -c 'import black' &> /dev/null
if [ $? -ne 0 ]; then
    echo "The 'black' python module was not found. Please try 'pip install black'."
    exit
fi

# Run checks.
BLACK_OUTPUT=$( (black --check src tests -v) 2>&1 )
STATUS=$?
if [ "$STATUS" -ne 0 ]; then
    echo "black checks failed:"
    echo "$BLACK_OUTPUT"
    echo "Please run 'black src tests'."
    exit "$STATUS"
else
    echo "black checks passed."
fi

RUFF_OUTPUT=$( (ruff check src tests) 2>&1 )
STATUS=$?
if [ "$STATUS" -ne 0 ]; then
    echo "ruff checks failed:"
    echo "$RUFF_OUTPUT"
    echo "Please fix ruff warning. (You could try 'ruff --fix src tests')"
    exit "$STATUS"
else
    echo "ruff checks passed."
fi
