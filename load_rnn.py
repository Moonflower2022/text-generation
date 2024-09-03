import torch
from torch import nn 
import os

def get_avaialable_file_name(file_name, extension):
    available_file_name = file_name
    i = 1
    while os.path.isfile(available_file_name + extension):
        available_file_name = file_name + f"_{i}"
        i += 1

    return available_file_name + extension

class GRUCharPredictor(nn.Module):
    def __init__(self):
        super(GRUCharPredictor, self).__init__()
        self.lstm = nn.GRU(input_size=INPUT_SIZE, hidden_size=256, num_layers=3, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(256 * 2, INPUT_SIZE)  

    def forward(self, x):
        lstm_out, _ = self.lstm(x)

        linear_out = self.fc(lstm_out[:, -1, :])

        return linear_out

class LSTMCharPredictor(nn.Module):
    def __init__(self):
        super(LSTMCharPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size=INPUT_SIZE, hidden_size=256, num_layers=3, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(256 * 2, INPUT_SIZE)  

    def forward(self, x):
        lstm_out, _ = self.lstm(x)

        linear_out = self.fc(lstm_out[:, -1, :])

        return linear_out

def encode_char(character): # one hot
    encoding = torch.zeros(INPUT_SIZE)
    encoding[CHARACTER_ENCODING[character]] = 1
    return encoding

def encode_string(string):
    encoding = torch.zeros(len(string), INPUT_SIZE)
    for i in range(len(string)):
        encoding[i] = encode_char(string[i])
    return encoding

def get_next_char(sequence, deterministic=False):
    logits = model(
        encode_string(sequence[-INPUT_SEQUENCE_LENGTH:]).unsqueeze(0)
    ) # returns in size (1, 78)

    probabilities = torch.softmax(logits[0], 0)

    character_index = torch.argmax(probabilities) if deterministic else torch.multinomial(probabilities, num_samples=1)
    
    return INDEX_ENCODING[int(character_index)]

def generate_text(starting_character, num_generated_characters):
    generated_text = starting_character

    with torch.no_grad():
        for _ in range(num_generated_characters):
            generated_text += get_next_char(generated_text)

    return generated_text

if __name__ == '__main__':
    text_name = "peter_pan"

    with open(f"texts/{text_name}.txt", "r") as file:
        text = file.read()

    print("# of characters:", len(text))

    unique_characters = set(text)
    INPUT_SIZE = len(unique_characters)
    print("# of unique characters (INPUT_SIZE):", INPUT_SIZE)

    ordered_characters = sorted(unique_characters)

    CHARACTER_ENCODING = dict(zip(ordered_characters, list(range(len(ordered_characters)))))

    INDEX_ENCODING = {}

    for char, i in CHARACTER_ENCODING.items():
        INDEX_ENCODING[i] = char

    print(INDEX_ENCODING)
    print(CHARACTER_ENCODING)

    INPUT_SEQUENCE_LENGTH = 5

    file_name = f"peter_pan_gru_{INPUT_SEQUENCE_LENGTH}chars"
    file_path = f"models/{file_name}.pth"

    model = GRUCharPredictor()
    model.load_state_dict(torch.load(file_path, weights_only=True))

    generated_text = generate_text("P", 1000)

    with open(
        get_avaialable_file_name(
            f"generated_texts/{file_name}", ".txt"
        ),
        "w",
    ) as file:
        file.write(generated_text)