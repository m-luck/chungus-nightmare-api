import random
import subprocess
import os
from pathlib import Path
from enum import Enum

class Punctuation(Enum):
    PERIOD = 1
    EXCLAMATION = 2
    DOUBLE_EXCLAMATION = 3
    NONE = 4

def get_gpt_output(prompt):
    generator_path = os.path.join(
        '.',
        'huggingface',
        'examples',
        'text-generation',
        'run_generation.py'
    )
    length = 400
    command = f'py {generator_path} --model_type gpt2 --model_name_or_path gpt2 --prompt "{prompt}" --length {length}'
    output = subprocess.check_output(command, shell=True)
    return output

def get_gpt_sequence(output):
    return str(output).split("=== GENERATED SEQUENCE 1 ===")[-1]

def split_into_sentences(sequence):
    return str(sequence).split(". ")
    
def get_punctuation(val):
    if val == Punctuation.PERIOD.value:
        return '.'
    if val == Punctuation.EXCLAMATION.value:
        return '!'
    if val == Punctuation.DOUBLE_EXCLAMATION.value:
        return '!!'
    if val == Punctuation.NONE.value:
        return ' '
    
def get_final_response(sentences, n=4):
    seed = random.randint(1,4)
    punctuation = get_punctuation(seed)
    return '. '.join(sentences[0:n-1]) + punctuation

def convert_newlines(text):
    return text.replace('\\n', '\n').replace('\\r', '\r')

def randomize_capitalization(text):
    seed = bool(random.getrandbits(1))
    if seed: 
        return text.lower()
    else: 
        return text

def char_swap(text):
    seed_a = random.randint(1, len(text)-1)
    seed_b = seed_a - 1
    seed = bool(random.getrandbits(1))
    if seed:
        text = list(text)
        text[seed_a], text[seed_b] = text[seed_b], text[seed_a]
        return ''.join(text)
    return text

def generate_response(prompt):
    n = random.randint(3,7)
    output = get_gpt_output(prompt)
    sequence = get_gpt_sequence(output)
    sentences = split_into_sentences(sequence)
    return convert_newlines(
        randomize_capitalization(
            char_swap(
                get_final_response(sentences, n)
            )
        )
    )