#! /usr/bin/bash

# source paths
SCRIPT_PATH=$(realpath "$0")
SOURCE_DIR=$(dirname "$SCRIPT_PATH")

# env, code and error file
PYTHON_ENV="$(cd "$SOURCE_DIR/../env/bin" && pwd)/python"
PYTHON_SCRIPT="$SOURCE_DIR/scripts/orders_generator.py"

# execute script
$PYTHON_ENV $PYTHON_SCRIPT 
