import os
import ollama
import pandas as pd
import argparse
import time
import logging
import csv
from post_processing import process_result, print_result

## python main.py --config config.txt

# Constants
RANDOM_STATE = 27

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_config(filename: str) -> dict:
    """Read the configuration from the specified file."""
    config = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        current_key = None
        for line in lines:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
                current_key = key.strip()
            elif current_key:
                config[current_key] += '\n' + line
            
    except FileNotFoundError:
        logging.error(f"Config file {filename} not found.")
    except Exception as e:
        logging.error(f"Error reading config file {filename}: {e}")
        
    return config

def read_csv(file_path: str, init_pos: int, end_pos: int) -> tuple[list[str], list[str]]:
    """Read a chunk of the CSV file and return lists of definitions and answers."""
    try:
        df = pd.read_csv(file_path)
        sampled_df = df.sample(n=len(df.index), random_state=RANDOM_STATE)
        df_chunk = sampled_df.iloc[init_pos:end_pos, :]
        definitions = df_chunk['definition'].tolist() 
        answers = df_chunk['answer'].tolist()
        
    except FileNotFoundError:
        logging.error(f"CSV file {file_path} not found.")
        definitions, answers = [], []
    except KeyError as e:
        logging.error(f"Missing column in CSV file {file_path}: {e}")
        definitions, answers = [], []
        
    return definitions, answers

def make_csv(filename: str, titles: list[str]) -> None:
    """Create a CSV file with the specified titles."""
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(titles)
    except Exception as e:
        logging.error(f"Error creating CSV file {filename}: {e}")

def make_csv_all(file_path: str) -> None:
    """Create right.csv, almost.csv, and wrong.csv in the specified directory."""
    make_csv(f"{file_path}/right.csv", ["CLUE", "ANS", "POS"])
    make_csv(f"{file_path}/almost.csv", ["CLUE", "ANS", "POS", "FOUND IN"])
    make_csv(f"{file_path}/wrong.csv", ["CLUE", "ANS", "OUTPUT"])
        
def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Run the script to interact with the Ollama model")
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--batch', help='Batch number')
    args = parser.parse_args()

    config = read_config(args.config)
    model = config.get('model')
    prompt = config.get('prompt')
    prompt_no = config.get('prompt_no')
    datasize = int(config.get('datasize'))
    
    if not prompt or not prompt_no or datasize == 0:
        logging.error("Missing required configuration values.")
        return
        
    batch = int(args.batch) # which process job we are on 
    init_pos = int(batch*datasize + 1) # which datapoint to start batch on
    end_pos = int(init_pos + datasize) # which datapoint to end batch on
    
    model_name = model.replace(':', '-')

    directory = f"outputs/{model_name}/prompt{prompt_no}/batch{batch}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    make_csv_all(directory)

    file_path = 'definitions.csv'
    definitions, answers = read_csv(file_path, init_pos, end_pos)
    
    if not prompt or not prompt_no or datasize == 0:
        logging.error("Missing required configuration values.")
        return
    
    right_count, almost_count = 0, 0
    
    start = time.time()
    for i in range(len(definitions)):
        logging.info(f"Processing {i+1}/{len(definitions)}")
        prompt_clue = prompt.replace('((def))', definitions[i])
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': f'{prompt_clue}',
            },
        ])
        
        generated_words = response['message']['content']
        logging.info(f"Definition: {definitions[i]}, Answer: {answers[i]}")
        logging.info(f"Generated words: {generated_words}")
        
        word_lines = generated_words[1:].splitlines()
        words_list = [line.split('. ')[1] for line in word_lines if '. ' in line]
        
        
        right_count,almost_count = process_result(
            definitions[i], answers[i], words_list, right_count, almost_count, directory
        )
        
    end = time.time()
    elapsed = end - start
    wrong_count = datasize - (right_count + almost_count)
                
    make_csv(f"{directory}/summary.csv", ["CHUNK", "RIGHT", "ALMOST", "WRONG", "TIME"])
    try:
        with open(os.path.join(directory, 'summary.csv'), "a", newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow([batch, right_count, almost_count, wrong_count, elapsed])
        logging.info("Summary has been written")
    except Exception as e:
        logging.error(f"Error writing summary CSV file: {e}")
    
if __name__ == "__main__":
    main()
