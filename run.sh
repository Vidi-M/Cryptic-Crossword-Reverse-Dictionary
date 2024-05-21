#!/usr/bin/bash

# Trap signals and ensure cleanup
trap 'trap - SIGTERM && kill -- -$$' SIGINT SIGTERM EXIT

# Store the current directory
current_dir=$(pwd)

# Check if a config file is provided as an argument
CONFIG_FILE="config.txt"  # Default config file
if [ $# -gt 0 ]; then
  CONFIG_FILE="$1"
fi

# Start the background service
cd ..
if [ -x Downloads/ollama ]; then
  Downloads/ollama serve &
else
  echo "Error: 'ollama' executable not found or not executable."
  exit 1
fi

# Change back to the original directory
cd "$current_dir" || exit

# Run the Python script with the specified config file
python main.py --config "$CONFIG_FILE"
