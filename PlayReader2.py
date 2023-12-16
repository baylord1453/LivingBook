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
    Parses a script and organizes the dialogue by characters, grouping a character's continuous dialogue as a single entry.

    Parameters:
    text (str): The content of the script.

    Returns:
    dict: A dictionary with character names as keys and a list of their dialogue blocks as values.
    """
    characters = {}
    current_character = None
    dialogue_block = ""

    for line in text.split('\n'):
        line = line.strip()
        # Check if the line is in uppercase (indicating a character's name)
        if line.isupper():
            # Save the previous character's dialogue block if it exists
            if current_character and dialogue_block:
                if current_character not in characters:
                    characters[current_character] = []
                characters[current_character].append(dialogue_block)
                dialogue_block = ""

            current_character = line
        elif current_character:
            # Accumulate the dialogue block for the current character
            if line:
                dialogue_block += line + " "  # Add a space to separate lines

    # Add the last character's dialogue block if it exists
    if current_character and dialogue_block:
        if current_character not in characters:
            characters[current_character] = []
        characters[current_character].append(dialogue_block)

    return characters


parsed_characters = parse_script_with_flexible_characters(script_content)

def find_preceding_dialogue(script, target_character, target_dialogue):
    """
    Finds the continuous dialogue of the character who spoke immediately before the target dialogue block.

    Parameters:
    script (dict): Parsed script with characters and their dialogues.
    target_character (str): The character whose dialogue block is targeted.
    target_dialogue (str): The specific dialogue block to find the preceding dialogue for.

    Returns:
    str: The preceding character's continuous dialogue block, or an empty string if not found.
    """
    previous_character = None
    previous_dialogue = ""

    for character, dialogues in script.items():
        for dialogue in dialogues:
            if character == target_character and dialogue == target_dialogue:
                return previous_dialogue
            previous_character = character
            previous_dialogue = dialogue

    return ""  # No preceding dialogue found

def find_following_dialogue(script, target_character, target_dialogue):
    """
    Finds the continuous dialogue of the character who speaks immediately after the target dialogue block.

    Parameters:
    script (dict): Parsed script with characters and their dialogues.
    target_character (str): The character whose dialogue block is targeted.
    target_dialogue (str): The specific dialogue block to find the following dialogue for.

    Returns:
    str: The following character's continuous dialogue block, or an empty string if not found.
    """
    found_target = False

    for character, dialogues in script.items():
        for dialogue in dialogues:
            if found_target and character != target_character:
                return dialogue  # Return the next dialogue spoken by a different character

            if character == target_character and dialogue == target_dialogue:
                found_target = True

    return ""  # No following dialogue found

import json

def create_training_data(parsed_characters, script_content):
    """
    Creates training data in JSONL format for each character.

    Parameters:
    parsed_characters (dict): Dictionary with characters and their dialogues.
    script_content (str): The full script content for context look-up.
    """
    for character, lines in parsed_characters.items():
        data = []
        for i, line in enumerate(lines):
            # Find preceding dialogue (user role)
            preceding_dialogue = find_preceding_dialogue(parsed_characters, character, line)

            # Find following dialogue (user role)
            following_dialogue = find_following_dialogue(parsed_characters, character, line)

            # Determine if the next dialogue is also by the same character (assistant role)
            next_assistant_line = ""
            if i + 1 < len(lines):
                next_assistant_line = lines[i + 1]

            # Structure the conversation snippet
            conversation = {
                "messages": [
                    {
                        "role": "user",
                        "content": preceding_dialogue
                    },
                    {
                        "role": "assistant",
                        "content": line
                    },
                    {
                        "role": "user",
                        "content": following_dialogue
                    }
                ]
            }

            # Add the next assistant line if applicable
            if next_assistant_line:
                conversation["messages"].append({
                    "role": "assistant",
                    "content": next_assistant_line
                })

            data.append(conversation)

        # Write to JSONL file
        jsonl_filename = f"{character}.jsonl"
        with open(jsonl_filename, 'w', encoding='utf-8') as file:
            for item in data:
                json.dump(item, file, ensure_ascii=False)
                file.write('\n')

        print(f"Data for {character} written to {jsonl_filename}")

create_training_data(parsed_characters, script_content)
