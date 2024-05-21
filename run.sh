#!/usr/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# Start the background service
cd ..
./Downloads/ollama serve &

# Back to correct directory
cd Cryptic-Crossword-Reverse-Dictionary

# Run the Python script with the specified config file

python main.py --config "$CONFIG_FILE"