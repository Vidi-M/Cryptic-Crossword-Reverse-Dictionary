#!/usr/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
./ollama serve &
python main.py --config config.txt