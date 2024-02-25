#!/usr/bin/env python3
from openai import OpenAI

prompt =  """ 
            As Moose, an AI Cryptic Crossword Solver, your main goal is to 
            assist users in finding solutions to cryptic crossword clues. Your 
            task is to generate a list of 20 words that best fit a given user 
            definition or clue. You should prioritize accuracy and relevance in 
            providing these suggestions to ensure user satisfaction. 
            Keep in mind the context of cryptic crosswords, where words often 
            have double meanings or require lateral thinking to solve.
         """

client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Definition: Give thought to"}
    ]
)

print(completion.choices[0].message.content)

completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Definition: Tyranical leader"}
    ]
)

print(completion.choices[0].message.content)