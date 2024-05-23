#!/bin/bash

# Trap signals and ensure cleanup
trap 'trap - SIGTERM && kill -- -$$' SIGINT SIGTERM EXIT

# Store the relevent directories
# Ollama directory
OLLAMA="/homes/${USER}/Downloads/ollama"
CROSSWORD="/homes/${USER}/Cryptic-Crossword-Reverse-Dictionary/"


# Check if a config file is provided as an argument
CONFIG_FILE="config.txt"  # Default config file
if [ $# -gt 0 ]; then
  CONFIG_FILE="$1"
fi


# Start the background service
if [ -x $OLLAMA ]; then
  $OLLAMA serve &
else
  echo "Error: 'ollama' executable not found or not executable."
  exit 1
fi

# Change back to the original directory
cd $CROSSWORD || exit

# Run the Python script with the specified config file
python main.py --config "config_test/$CONFIG_FILE"
