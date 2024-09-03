import random
import string
import os

def create_chain(training_data):
    markov_chain = {}

    for sequence, next in training_data:
        if sequence in markov_chain:
            markov_chain[sequence] += [next]
        else: # not sequence in markov_chain
            markov_chain[sequence] = [next]

    return markov_chain

def get_result_from_chain(markov_chain, sequence):
    if sequence in markov_chain:
        return random.choice(markov_chain[sequence])
    else:
        print(f"unknown sequence {sequence}")
        return random.choice(string.ascii_letters)
    
def generate_text():
    with open(f"texts/{TEXT_NAME}.txt", "r") as file:
        text = file.read()

    print("# of characters:", len(text))

    sequences = []

    for i in range(len(text) - SEQUENCE_LENGTH):
        sequences.append((text[i : i + SEQUENCE_LENGTH], text[i + SEQUENCE_LENGTH]))

    markov_chain = create_chain(sequences)

    generated_text = random.choice(list(markov_chain.keys())) # "".join([random.choice(text) for _ in range(SEQUENCE_LENGTH)])

    for i in range(NUM_GENERATED_CHARACTERS):
        generated_text += get_result_from_chain(markov_chain, generated_text[-SEQUENCE_LENGTH:])

    print(generated_text)

    return generated_text

def get_avaialable_file_name(file_name, extension):
    available_file_name = file_name
    i = 1
    while os.path.isfile(available_file_name + extension):
        available_file_name = file_name + f"_{i}"
        i += 1

    return available_file_name + extension

if __name__ == '__main__':
    SEQUENCE_LENGTH = 15
    print("sequence length:", SEQUENCE_LENGTH)
    TEXT_NAME = "python_snippets"
    NUM_GENERATED_CHARACTERS = 1000
    NUM_GENERATED_SEQUENCES = 1
    for _ in range(NUM_GENERATED_SEQUENCES):
        generated_text = generate_text()

        with open(get_avaialable_file_name(f"generated_texts/{TEXT_NAME}_markov_chain_{SEQUENCE_LENGTH}chars", ".txt"), "w") as file:
            file.write(generated_text)