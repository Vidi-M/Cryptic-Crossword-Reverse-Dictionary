import os
import csv


def process_result(clue, answer, words, right_count, almost_count, dir):
    ## Check for match with answer
    page = 'wrong'
    chars = len(answer)
    for pos, word in enumerate(words):
        word_lower = word.lower()
        if word_lower == answer and page != 'right':
            page = 'right'
            # printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} \n"
            result = [clue, answer, pos+1]
            
        for i in range(len(word_lower) - chars + 1):
            substring = word_lower[i:i+chars]  # Get a substring of the word with the same length as the answer
            if substring == answer and page != 'almost' and page != 'right':
                page = 'almost'
                # printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} ||| Found in: {word} \n"
                result = [clue, answer, pos+1, word]
        
    if page == 'wrong':
        # printline = f"CLUE: {clue} ||| ANS: {answer} \n {words} \n"
        result = [clue, answer, words]
    
    ### Write to file
    if page == 'right':
        output_filename = 'right.csv'
        right_count += 1
    elif page == 'almost':
        output_filename = 'almost.csv'
        almost_count += 1
    else:
        output_filename = 'wrong.csv'

    with open(os.path.join(dir, output_filename), 'a', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(result)

    return right_count, almost_count

def print_result(chunk, right_count, almost_count, time, dir):
    # results = (
    #     "-------------------------------------------------\n"
    #     f"RIGHT: {right_count / length * 100:.2f}%\n"
    #     f"ALMOST: {almost_count / length * 100:.2f}%\n"
    #     f"ACCURACY: {(right_count + almost_count) / length * 100:.2f}%\n"
    #     f"TIME ELAPSED: {time}\n"
    #     "-------------------------------------------------\n"
    # )

                
    with open(os.path.join(dir, 'summary.csv'), "a", newline= '') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(chunk, right_count, almost_count)