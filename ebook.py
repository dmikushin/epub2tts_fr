import re
import subprocess

def process_number(number):
    # Remove spaces between digits
    number = re.sub(r'\s+', '', number)
    command = f'number-to-words --lang=fr {number}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    text = output.decode('utf-8').strip()
    print(text)
    return f' {text} '

def find_replace_numbers(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Replace all numbers with a written text equivalents
    text = re.sub(r'(\d[\d\s]*)', lambda x: process_number(x.group()), text)

    # Write the replaced text back to the file
    with open(file_path, 'w') as file:
        file.write(text)


# Example usage
find_replace_numbers('./oceania.txt')
