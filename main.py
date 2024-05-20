import os
import ollama
import pandas as pd
import argparse
import time
from post_processing import process_result, print_result

## python main.py --config config.txt

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

def read_csv(file_path, dataset): ## need to implement cross validation
    df = pd.read_csv(file_path)
    sampled_df = df.sample(n=dataset, random_state=27)
    definitions = sampled_df['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = sampled_df['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
    #word_lengths = [len(word) for answer in answers for word in answer.split()]
    return definitions, answers
    right = False
    for pos, word in enumerate(words):
        if word.lower() == answer and right != True:
            right = True
            printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} \n"
    if right == False:
        printline = f"CLUE: {clue} ||| ANS: {answer} \n {words} \n"
    
    return right, printline

def main():
    parser = argparse.ArgumentParser(description="Run the script to interact with the Ollama model")
    parser.add_argument('--config', help='Path to config file')
    args = parser.parse_args()

    config = read_config(args.config)
    model = config.get('model', 'llama2')  # Default to 'llama2' if not specified
    prompt = config.get('prompt')
    prompt_no = config.get('prompt_no')
    dataset = int(config.get('dataset'))
    
    directory = f"prompt{prompt_no}/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = 'definitions.csv'
    definitions, answers = read_csv(file_path, dataset)
    right_count, almost_count = 0, 0
    
    start = time.time()
    for i in range(len(definitions)):
        print(f"{i+1}/{len(definitions)}")
        prompt = prompt.replace('{definition}', definitions[i])
        print(prompt)
        response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
        ])
        
        generated_words = response['message']['content']
        
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
                
    print_result(right_count, almost_count, len(definitions), elapsed, directory)
    
if __name__ == "__main__":
    main()