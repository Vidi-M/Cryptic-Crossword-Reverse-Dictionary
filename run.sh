#!/bin/bash

# Store the relevent directories
# Ollama directory
OLLAMA="/homes/${USER}/Downloads/"
CROSSWORD="/homes/${USER}/Cryptic-Crossword-Reverse-Dictionary/"


# Check if a config file is provided as an argument
CONFIG_FILE="config.txt"  # Default config file
if [ $# -gt 0 ]; then
  CONFIG_FILE="$1"
fi


# Go to ollama directory
cd $OLLAMA || echo "Error: can't reach OLLAMA directory"; exit 1

# Start the background service
if [ -x ./ollama ]; then
  ./ollama serve &
else
  echo "Error: 'ollama' executable not found or not executable."
  exit 1
fi

# Change back to the original directory
cd $CROSSWORD || exit

# Run the Python script with the specified config file
python main.py --config "config_test/$CONFIG_FILE"
