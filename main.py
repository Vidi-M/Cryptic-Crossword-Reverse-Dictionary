import os
import ollama
import pandas as pd
import argparse
import time
import datetime
import csv
from post_processing import process_result, print_result

## python main.py --config config.txt

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split('=')
                config[key.strip()] = value.strip()
    return config

def read_csv(file_path, datasize, init_pos): ## need to implement cross validation
    df = pd.read_csv(file_path)
    sampled_df = df.sample(random_state=27)
    df_chunk = sampled_df['definition'][init_pos: init_pos + datasize]
    definitions = df_chunk['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = df_chunk['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
    #word_lengths = [len(word) for answer in answers for word in answer.split()]
    return definitions, answers

def make_csv(filename, titles):
    with open(filename, 'w', newline='') as file:
        c = csv.writer(filename)
        c.writerow(titles)

def make_csv_all(file_path):
    make_csv(f"{file_path}/right.csv", ["CLUE", "ANS", "POS"])
    make_csv(f"{file_path}/almost.csv", ["CLUE", "ANS", "POS", "FOUND IN"])
    make_csv(f"{file_path}/wrong.csv", ["CLUE", "ANS", "OUTPUT"])
    make_csv(f"{file_path}/summary.csv", ["CHUNK", "RIGHT", "ALMOST", "WRONG", "TIME"])
        
def main():
    parser = argparse.ArgumentParser(description="Run the script to interact with the Ollama model")
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--machines', help='Number of machines it is running on')
    parser.add_argument('--chunk', help='Chunk number')
    args = parser.parse_args()
    date = datetime.date.today()

    config = read_config(args.config)
    model = config.get('model', 'llama2')  # Default to 'llama2' if not specified
    prompt = config.get('prompt')
    prompt_no = config.get('prompt_no')
    datasize = int(config.get('datasize'))
    batch = int(config.get('batch')) # Which section it is in
    
    #
    machines = args.machines
    chunk = args.chunk #which parallel job it is
    init_pos = (machines*datasize*batch) + (chunk * datasize)
    
    directory = f"{model}-{date}/prompt{prompt_no}/batch{batch}-chunk{chunk}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    make_csv_all(directory)

    file_path = 'definitions.csv'
    definitions, answers = read_csv(file_path, datasize, init_pos)
    
    right_count, almost_count = 0, 0
    
    start = time.time()
    for i in range(len(definitions)):
        print(f"{i+1}/{len(definitions)}")
        prompt_clue = prompt.replace('{def}', definitions[i])
        response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': f'{prompt_clue}',
        },
        ])
        
        generated_words = response['message']['content']
        
        print(generated_words)
        
        word_lines = generated_words[1:].splitlines()
        words_list = [line.split('. ')[1] for line in word_lines if '. ' in line]
        
        
        
        
        right_count,almost_count = process_result(definitions[i], 
                                                  answers[i], 
                                                  words_list, 
                                                  right_count, 
                                                  almost_count,
                                                  directory)
        
    end = time.time()
    elapsed = end - start
    wrong_count = datasize - (right_count + almost_count)
                
    # print_result(right_count, almost_count, len(definitions), elapsed, directory)
    
    with open(os.path.join(directory, 'summary.csv'), "w", newline= '') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(batch, chunk, right_count, almost_count, wrong_count, elapsed)
    
if __name__ == "__main__":
    main()