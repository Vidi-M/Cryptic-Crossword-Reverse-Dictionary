#!/usr/bin/env python3
from openai import OpenAI
import pandas as pd

def read_csv(file_path):
    df = pd.read_csv(file_path)
    definitions = df['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = df['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
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
            
            

file_path = 'definitions.csv'
definitions, answers = read_csv(file_path)
right_count = 0
wrong_count = 0

prompt =  """ 
            You are a crossword solver. You will take in a user definition and return a list of 20 words that match the definition. The output must be a list of 20 words seperated by commas.
            
            An example of the input and output: 
            input: Tyrannical Ruler
            output: Dictator, Despot, Autocrat, Ruler, Tyrant, Potty, Big Brother, Boss, Overlord, Emperor, King, Queen, Pope, Cardinal, General, Chairman, President, Prime Minister, Secretary-General, Chancellor
         """

client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

for i in range(len(definitions)):
    print(f"{i+1} / {len(definitions)}")

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            #{"role": "system", "content": prompt},
            {"role": "user", "content": f"You are a crossword solvefr, Give me a list of 20 words that match this Definition: {definitions[i]}"}
        ]
    )

    generated_words = completion.choices[0].message.content
    # Split the string into lines
    word_lines = generated_words[1:].splitlines()
    # Split each line into words
    words_list = [line.split('. ')[1] for line in word_lines]
    
    right, printline = write_info(definitions[i], answers[i], words_list)
    
    if right == True:
        output_filename = 'right_results.txt'
        right_count += 1
    else:
        output_filename = 'wrong_results.txt'
        
    with open(output_filename, 'a') as output_file:
            output_file.write(printline)
    
print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
print(f"ACCURACY: {right_count/ len(definitions) * 100}%")
print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")