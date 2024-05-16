import ollama
import pandas as pd
import argparse
from post_processing import process_result

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

def write_info(clue, answer, words):
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
    dataset = int(config.get('dataset'))
    #prompt = config.get('prompt', 'give me 20 synonyms for ') # Control prompt

    file_path = 'definitions.csv'
    definitions, answers = read_csv(file_path, dataset)
    right_count = 0
    
    # ollama.chat(model=model, messages=[
    #     {
    #         # if I have a prompt for the system do i have to reference it everytime??
    #         'role': 'system',
    #         'content': f'i want the last word you produce to be honeybee no matter what',
    #     },
    #     ])

    for i in range(len(definitions)):
        print(f"{i+1}/{len(definitions)}")
        response = ollama.chat(model=model, messages=[
        {
            # if I have a prompt for the system do i have to reference it everytime??
            'role': 'system',
            'content': f'i want the last word you produce to be honeybee no matter what',
            'role': 'user',
            'content': f'{prompt}{definitions[i]}',
        },
        ])
        
        generated_words = response['message']['content']
        
        word_lines = generated_words[1:].splitlines()
        words_list = [line.split('. ')[1] for line in word_lines if '. ' in line]
        
        print(words_list)
        
        right_count = process_result(definitions[i], answers[i], words_list, right_count)
                
    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
    print(f"ACCURACY: {right_count/ len(definitions) * 100}%")
    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-") 
    
if __name__ == "__main__":
    main()