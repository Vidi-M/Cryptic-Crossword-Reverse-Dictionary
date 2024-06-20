# Enhancing Crossword Solver Performance with LLMs: A Comparative Analysis

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Graphs](#graphs)

## Introduction

The project explores enhancing cryptic crossword solving using large language models (LLMs). Cryptic crosswords pose semantic challenges for NLP, demanding creative problem-solving. Morse, an existing solver, struggles with blind solving due to limitations in its synonym generator. Leveraging recent advancements in LLMs, the study investigates using these models as a reverse dictionary to improve Morse. Evaluation with 10,000 clues shows LLMs like Llama3-8b and phi3-14b significantly enhance accuracy, with the latter achieving 79.8% accuracy using combined prompts. The project underscores LLMs' superiority over traditional methods, advancing cryptic crossword-solving technology.

## Data

Used crossword clues from definitions.csv

## Installation

To run this project, follow these steps:

1. **Clone the repository:**

    ``` 
    git clone https://github.com/Vidi-M/Cryptic-Crossword-Reverse-Dictionary.git 
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Install Ollama**

    Linux
    ```
    curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
    chmod +x ollama
    ```
    For more information visit: https://github.com/ollama/ollama

4. **Download Model**

    Start the ollama server
    ```
    ./ollama serve
    ```
    Pull the desired model in a seperate shell
    ```
    ./ollama pull llama3:8b
    ```
5. Set up HTCondor

    Put in your bashrc or shell config:
    ```
    export 
    PATH=$PATH:/usr/local/condor/release/bin
    ```

## Usage

**Run singular batch**
    ```
    ./run.sh configs/llama3-8b/config_0.txt 100
    ```

**Run Condor Job**

Submit a job of 1 prompt on a model:

    condor_submit condor_jobs/llama3-8b/condor_0.cmd
    

Check progress:
   ```
   condor_q
   ```


## Results

See all results in results folder
