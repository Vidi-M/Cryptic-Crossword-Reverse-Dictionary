def process_result(clue, answer, words, right_count):
    right = False
    for pos, word in enumerate(words):
        if word.lower() == answer and not right:
            right = True
            printline = f"CLUE: {clue} ||| ANS: {answer} ||| POS: {pos+1} \n"
            break
    else:
        printline = f"CLUE: {clue} ||| ANS: {answer} \n {words} \n"

    if right:
        output_filename = 'right_results.txt'
        right_count += 1
    else:
        output_filename = 'wrong_results.txt'

    with open(output_filename, 'a') as output_file:
        output_file.write(printline)

    return right_count
