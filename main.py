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
    with open(filename, 'r') as file:
        lines = file.readlines()

    config = {}
    current_key = None

    for line in lines:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
            current_key = key.strip()
        elif current_key:
            config[current_key] += '\n' + line

    return config

def read_csv(file_path, init_pos, end_pos): ## need to implement cross validation
    df = pd.read_csv(file_path)
    sampled_df = df.sample(n=len(df.index), random_state=27)
    df_chunk = sampled_df.iloc[init_pos:end_pos, :]
    definitions = df_chunk['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = df_chunk['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
    #word_lengths = [len(word) for answer in answers for word in answer.split()]
    return definitions, answers

def make_csv(filename, titles):
    with open(filename, 'w', newline='') as file:
        c = csv.writer(file)
        c.writerow(titles)

def make_csv_all(file_path):
    make_csv(f"{file_path}/right.csv", ["CLUE", "ANS", "POS"])
    make_csv(f"{file_path}/almost.csv", ["CLUE", "ANS", "POS", "FOUND IN"])
    make_csv(f"{file_path}/wrong.csv", ["CLUE", "ANS", "OUTPUT"])
        
def main():
    parser = argparse.ArgumentParser(description="Run the script to interact with the Ollama model")
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--chunk', help='Chunk number')
    args = parser.parse_args()
    date = datetime.date.today()

    config = read_config(args.config)
    model = config.get('model', 'llama2')  # Default to 'llama2' if not specified
    prompt = config.get('prompt')
    prompt_no = config.get('prompt_no')
    datasize = int(config.get('datasize'))
        
    chunk = int(args.chunk) #which process job it is
    init_pos = int(chunk*datasize + 1)
    end_pos = int(init_pos + datasize)

    directory = f"{model}/prompt{prompt_no}/chunk{chunk}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    make_csv_all(directory)

    file_path = 'definitions.csv'
    definitions, answers = read_csv(file_path, init_pos, end_pos)
    

    right_count, almost_count = 0, 0
    
    start = time.time()
    for i in range(len(definitions)):
        print(f"{i+1}/{len(definitions)}")
        prompt_clue = prompt.replace('((def))', definitions[i])
        response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': f'{prompt_clue}',
        },
        ])
        
        generated_words = response['message']['content']
        
        print(f"def: {definitions[i]} ans: {answers[i]}")
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
    make_csv(f"{file_path}/summary.csv", ["CHUNK", "RIGHT", "ALMOST", "WRONG", "TIME"])
    
    with open(os.path.join(directory, 'summary.csv'), "a", newline= '') as output_file:
        writer = csv.writer(output_file)
        writer.writerow([chunk, right_count, almost_count, wrong_count, elapsed])
        
    print("summary has been written")
    
if __name__ == "__main__":
    main()
