# A set of Python scripts for editing text file with e-book to form, suitable for a synthesis with Piper dialog system

import sys
import nltk

#nltk.download('punkt')

def remove_empty_lines(path):
    
    with open(path, 'r') as file:
        text = file.readlines()

    text = list(filter(lambda s: s != "\n", text))

    with open(path, 'w') as file:
        file.writelines(text)

    print(f"Empty lines deleted in {path}.")


def split_long_lines(path):

    with open(path, "r") as file:
        text = file.read()
        text_split = text.splitlines()

        for line, index_line in zip(text_split, range(len(text_split))):
            
            # 3000 chars is value under upper threshold that piper can synthesise for one epoch
            if len(line) >= 3000:
                # Split line to sentences
                sentences = nltk.sent_tokenize(line)
                counter = 0

                for sentence, index_sentence in zip(sentences, range(len(sentences))):
                    counter += len(sentence)

                    if counter >= 3000:
                        sentences.insert(index_sentence, "\n")
                        counter = 0

                text_split[index_line] = " ".join(sentences)

        text = "\n".join(text_split)

    with open(path, "w") as file:
        file.write(text)

    print(f"Lines longer than 1000 splitted to multiple lines in {path}.")


def strip_lines(path):

    with open(path, "r") as file:
        text_split = file.readlines()

        for line, index in zip(text_split, range(len(text_split))):
            text_split[index] = line.strip()
    
    with open(path, "w") as file:
        text = "\n".join(text_split)
        file.write(text)

    print(f"White spaces removed in {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 preprocessing.py <input_file>")
        exit(1)

    path = sys.argv[1]

    try:
        with open(path, 'r') as file:
            pass
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        exit(1)

    print(f"Editing file '{path}'...")
    remove_empty_lines(path)
    split_long_lines(path)
    strip_lines(path)