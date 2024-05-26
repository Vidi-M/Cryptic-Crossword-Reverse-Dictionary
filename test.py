def read_prompt_from_config(config_file):
    with open(config_file, 'r') as file:
        lines = file.readlines()
    
    prompt = ""
    capture = False
    
    for line in lines:
        if line.startswith("prompt="):
            prompt = line[len("prompt="):].strip()
            capture = True
        elif capture and line.startswith("model="):
            break
        elif capture:
            prompt += "\n" + line.strip()
    
    return prompt

def main():
    config_file = 'test.txt'  # Replace with your actual config file name
    prompt = read_prompt_from_config(config_file)
    
    if prompt:
        print("Extracted Prompt:")
        print(prompt)
    else:
        print("No prompt found in the config file.")

if __name__ == "__main__":
    main()
