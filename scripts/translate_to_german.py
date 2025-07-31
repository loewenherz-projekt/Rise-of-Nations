import os
import re
import sys
from google.cloud import translate_v2 as translate

client = translate.Client()
pattern = re.compile(r'^(\s*[^#\s][^:]*:\d+\s*")(.*)(".*)$')

def translate_line(line: str) -> str:
    match = pattern.match(line)
    if match:
        prefix, text, suffix = match.groups()
        try:
            translated = client.translate(text, target_language='de')
            translated_text = translated['translatedText']
        except Exception:
            translated_text = text
        return f"{prefix}{translated_text}{suffix}\n"
    if line.strip() == 'l_english:' or line.strip() == '\ufeffl_english:':
        return line.replace('l_english', 'l_german')
    return line


def translate_file(eng_path: str, ger_path: str):
    with open(eng_path, 'r', encoding='utf-8-sig') as f:
        lines = [translate_line(line) for line in f]
    with open(ger_path, 'w', encoding='utf-8') as out:
        out.writelines(lines)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: translate_to_german.py <english_file> <german_file>")
        sys.exit(1)
    translate_file(sys.argv[1], sys.argv[2])
