import os
import re
import sys
from pathlib import Path
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
    # translate the header line l_english:
    if line.strip() == 'l_english:' or line.strip() == '\ufeffl_english:':
        return line.replace('l_english', 'l_german')
    return line


def translate_file(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with src.open('r', encoding='utf-8-sig') as f:
        lines = [translate_line(line) for line in f]
    with dest.open('w', encoding='utf-8') as out:
        out.writelines(lines)


def translate_directory(src_dir: Path, dest_dir: Path):
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.yml'):
                src_path = Path(root) / file
                rel = src_path.relative_to(src_dir)
                dest_path = dest_dir / rel
                dest_path = Path(str(dest_path).replace('_l_english', '_l_german'))
                translate_file(src_path, dest_path)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: translate_directory_to_german.py <english_dir> <german_dir>')
        sys.exit(1)
    translate_directory(Path(sys.argv[1]), Path(sys.argv[2]))
