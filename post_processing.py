def process_result(clue, answer, words, right_count, almost_count):
    ## Check for match with answer
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
    
    ### Write to file
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

    return right_count, almost_count
