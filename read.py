import pandas as pd

def read_csv(file_path, nrows=10):
    df = pd.read_csv(file_path, nrows=nrows)
    definitions = df['definition'].tolist()  # Assuming 'Definition' is the header for the definition column
    answers = df['answer'].tolist()  # Assuming 'Answer' is the header for the answer column
    return definitions, answers

# Example usage:
file_path = 'definitions.csv'
definitions, answers = read_csv(file_path)
print("Definitions:", definitions)
print("Answers:", answers)

## 20 words: Dictator, Despot, Autocrat, Ruler, Tyrant, Potty, Big Brother, Boss, Overlord, Emperor, King, Queen, Pope, Cardinal, General, Chairman, President, Prime Minister, Secretary-General, Chancellor