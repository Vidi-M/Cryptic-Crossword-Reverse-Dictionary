import csv
import random
from openai import OpenAI

def load_definitions(filename):
    """Load definitions and answers from a CSV file."""
    definitions = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            definitions.append((row['definition'], row['answer']))
    return definitions[:2]  # Load only the first 10 definitions for testing

def get_answer_position(answers, generated_words):
    """Check if any of the generated words match the answer."""
    found_count = 0
    for idx, word in enumerate(generated_words):
        if word in answers:
            found_count += 1
    return found_count, found_count / len(answers) * 100 if answers else 0

# Load definitions and answers from CSV
definitions = load_definitions('definitions.csv')

prompt = """ 
            As Moose, an AI Cryptic Crossword Solver, your main goal is to 
            assist users in finding solutions to cryptic crossword clues. Your 
            task is to generate a list of 20 words or phrases that best fit a given user 
            definition or clue. You should prioritize accuracy and relevance in 
            providing these suggestions to ensure user satisfaction. 
            Keep in mind the context of cryptic crosswords, where words often 
            have double meanings or require lateral thinking to solve.
            Example of a clue would be: readily available = on tap, Left hungry = unfed
         """

# Choose a random definition from the loaded definitions
definition, answer = random.choice(definitions)

client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key="sk-no-key-required"
)

user_input = f"{definition}"
completion = client.chat.completions.create(
    model="text-davinci-003",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]
)

generated_words = completion.choices[0].message
print(generated_words)

# Check how many answers are found and calculate the percentage
found_count, percentage_found = get_answer_position(answer.split(), generated_words)

# Write the result to a file
output_filename = 'result.txt'
with open(output_filename, 'w') as output_file:
    if found_count:
        output_file.write(f"The answer '{answer}' was found {found_count} times out of 20.\n")
        output_file.write(f"Percentage of answers found: {percentage_found:.2f}%\n")
    else:
        output_file.write(f"Clue: {definition}\n")
        output_file.write(f"Generated words: {', '.join(str(generated_words))}\n")

print(f"Result written to {output_filename}.")
