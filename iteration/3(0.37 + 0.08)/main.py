#!/usr/bin/env python3
from openai import OpenAI
import pandas as pd
import time


def read_csv(file_path, nrows=100):
    df = pd.read_csv(file_path, nrows=nrows)
    definitions = df['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = df['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
    #word_lengths = [len(word) for answer in answers for word in answer.split()]
    return definitions, answers

def stars(word):
    star = ''
    for char in word:
        if char == ' ':
            star += '-'
        else:
            star += '*'
    return star

def write_info(clue, answer, words):
    page = 'wrong'
    chars = len(answer)
    for pos, word in enumerate(words):
        word_lower = word.lower()
        if word_lower == answer and page != 'right':
            page = 'right'
            printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} \n"
            
        for i in range(len(word_lower) - chars + 1):
            substring = word_lower[i:i+chars]  # Get a substring of the word with the same length as the answer
            if substring == answer and page != 'almost' and page != 'right':
                page = 'almost'
                printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} ||| Found in: {word} \n"
        
    if page == 'wrong':
        printline = f"CLUE: {clue} ||| ANS: {answer} \n {words} \n"
    
    return page, printline
            
            

file_path = 'definitions.csv'
definitions, answers = read_csv(file_path)
right_count = 0
almost_count = 0


client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

for i in range(len(definitions)):
    start = time.time()
    print(f"{i+1} / {len(definitions)}")
    word_length = [len(word) for word in answers[i].split()]
    print(word_length)

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            #{"role": "system", "content": prompt},
            {"role": "user", "content": f"I need help with a crossword clue, the clue is {definitions[i]} and these are the letters I know ({stars(answers[i])}) where the * mean unknown letters and the - means a whitespace. Give me 20 words or phrases that match this information"}
            #{"role": "user", "content": f"I need help with a crossword clue, the clue is {definitions[i]} and these are the letters I know ({stars(answers[i])}) where the * mean unknown letters and the - means a whitespace. Give me 20 words or phrases that match the clue and letters. You should prioritize accuracy and relevance in providing these suggestions to ensure user satisfaction. Keep in mind the context of cryptic crosswords, where words often have double meanings or require lateral thinking to solve."}
        ]
    )

    generated_words = completion.choices[0].message.content
    end = time.time()
    # Split the string into lines
    word_lines = generated_words[1:].splitlines()
    # Split each line into words
    words_list = [line.split('. ')[1] for line in word_lines if '. ' in line]
    
    
    
    print(stars(answers[i]))
    print(end-start)
    
    page, printline = write_info(definitions[i], answers[i], words_list)
    
    if page == 'right':
        output_filename = 'right_results.txt'
        right_count += 1
    elif page == 'almost':
        output_filename = 'almost_results.txt'
        almost_count += 1
    else:
        output_filename = 'wrong_results.txt'
        
    with open(output_filename, 'a') as output_file:
            output_file.write(printline)
    
print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
print(f"RIGHT: {right_count/ len(definitions) * 100}%")
print(f"ALMOST: {almost_count/ len(definitions) * 100}%")
print(f"ACCURACY: {right_count + almost_count/ len(definitions) * 100}%")
print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")