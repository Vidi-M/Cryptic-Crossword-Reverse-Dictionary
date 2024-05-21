#!/usr/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# Start the background service
..Downloads/ollama serve &

# Run the Python script with the specified config file
python main.py --config "$CONFIG_FILE"