#!/usr/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
..Downloads/ollama serve &
python main.py --config config.txt