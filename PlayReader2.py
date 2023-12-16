from xml.dom.pulldom import CHARACTERS
import PyPDF2
import pytesseract
from PIL import Image
import io
import json

def read_script(file_path):
    """
    Reads a script from a given file path and returns its content as a string.

    Parameters:
    file_path (str): The path to the script file.

    Returns:
    str: The content of the script.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

file_path = "rj.txt"  # Replace with the actual path to your script
script_content = read_script(file_path)
if script_content:
    print("Script read successfully.")

def parse_script_with_flexible_characters(text):
    """
    Parses a script and organizes the dialogue by characters.

    Parameters:
    text (str): The content of the script.

    Returns:
    dict: A dictionary with character names as keys and a list of their lines as values.
    """
    characters = {}

    current_character = None
    for line in text.split('\n'):
        line = line.strip()
        # Check if the line is in uppercase (indicating a character's name)
        if line.isupper():
            current_character = line
            # Add the character to the dictionary if not already present
            if current_character not in characters:
                characters[current_character] = []
        elif current_character:
            # Add the line to the current character's dialogue, excluding empty lines
            if line:
                characters[current_character].append(line)

    return characters

parsed_characters = parse_script_with_flexible_characters(script_content)

def create_training_data(parsed_characters):
    """
    Creates training data in JSONL format for each character.

    Parameters:
    parsed_characters (dict): Dictionary with characters and their dialogues.
    """
    for character, lines in parsed_characters.items():
        # Prepare data for JSONL
        data = []
        for i in range(1, len(lines)):
            conversation_pair = {
                "input": lines[i - 1],
                "response": lines[i]
            }
            data.append(conversation_pair)

        # Write to JSONL file
        jsonl_filename = f"{character}.jsonl"
        with open(jsonl_filename, 'w', encoding='utf-8') as file:
            for item in data:
                json.dump(item, file)
                file.write('\n')

        print(f"Data for {character} written to {jsonl_filename}")

create_training_data(parsed_characters)

# # Example usage
# # Replace 'rj.jsonl' with the path to your .jsonl file

# def parse_play(text):
#     # Dictionary with character names as keys and empty lists for their lines
#     characters = {
#         "ROMEO": [],
#         "MONTAGUE": [],
#         "LADY MONTAGUE": [],
#         "ABRAM": [],
#         "BALTHASAR": [],
#         "JULIET": [],
#         "CAPULET": [],
#         "LADY CAPULET": [],
#         "TYBALT": [],
#         "PETRUCHIO": [],
#         "SAMPSON": [],
#         "GREGORY": [],
#         "PETER": [],
#         "ESCALUS": [],
#         "PARIS": [],
#         "MERCUTIO": [],
#         "FRIAR LAWRENCE": [],
#         "FRIAR JOHN": [],
#         "APOTHECARY": []
#     }

#     current_character = None
#     for line in text.split('\n'):
#         line = line.strip()
#         if line in characters:
#             current_character = line
#         elif current_character:
#             characters[current_character].append(line)

#     return characters

# # Example usage
# # Assuming 'play_text' is a string containing the entire text of the play
# # parsed_characters = parse_play(play_text)

# # Example usage
# pdf_path = 'rj.pdf'
# extracted_text = extract_text_from_pdf(pdf_path)
# print(extracted_text)

# import json
# from transformers import GPT2Tokenizer
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import sent_tokenize

# def clean_text(text):
#     # Replace Unicode characters with ASCII equivalents or remove them
#     replacements = {
#         '\u2014': '-',  # Replace em dash with hyphen
#         '\u201c': '"',  # Replace left double quotation mark with standard quotation
#         '\u201d': '"',  # Replace right double quotation mark with standard quotation
#         # Add more replacements as needed
#     }
#     for unicode_char, ascii_char in replacements.items():
#         text = text.replace(unicode_char, ascii_char)
#     return text

# # Example usage
# text=extracted_text
# grouped_sentences = segment_text(text)
# write_segments_to_jsonl(grouped_sentences, 'RJ.jsonl')

# import re
# import json

# def read_script(file_path):
# # Code to read the script file
# pass

# def parse_script(content):
# # Code to parse the script and extract characters and dialogues
# pass

# def script_to_json(parsed_data):
# # Convert the parsed data to JSON format
# return json.dumps(parsed_data, indent=4)

# # Main function to tie everything together
# def main():
# file_path = "path_to_script.txt"  # Replace with your script path
# script_content = read_script(file_path)
# parsed_data = parse_script(script_content)
# script_json = script_to_json(parsed_data)

# # Save the JSON to a file
# with open("script_output.json", "w") as file:
#     file.write(script_json)

# if __name__ == "__main__":
# main()
