#!/usr/bin/bash

# Store the relevent directories
CROSSWORD="/homes/${USER}/Cryptic-Crossword-Reverse-Dictionary/"


# Check if a config file is provided as an argument
CONFIG_FILE="config.txt"  # Default config file
BATCH=300 #default batch number
if [ $# -gt 0 ]; then
  CONFIG_FILE="$1"
  BATCH="$2"
fi

# Start the background service
if [ -x ./ollama ]; then
  ./ollama serve & echo "{"$BATCH"}: Sucess: 'ollama' server  executed"
else
  echo "Error: 'ollama' executable not found or not executable."
  exit 1
fi

# Add a time delay for the ollama model to get ready
sleep 8

# Run the Python script with the specified config file
python main.py --config "$CONFIG_FILE" --batch "$BATCH"|| echo "{"$BATCH"}: Error: main.py did not execute"
