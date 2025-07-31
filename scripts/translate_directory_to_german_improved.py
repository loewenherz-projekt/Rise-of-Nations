import os
import re
import sys
import threading
import signal
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import time

from google.cloud import translate_v2 as translate
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/cloud-translation"]
TOKEN_FILE = "token.json"
CLIENT_SECRETS_FILE = "client_secret.json"

# Thread-local storage for translate clients
_thread_local = threading.local()

# Global shutdown event for graceful interruption
shutdown_event = threading.Event()

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print("\n⚠️  Interruption received. Shutting down gracefully...")
    print("   Please wait for current translations to complete...")
    shutdown_event.set()

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, signal_handler)

def get_credentials():
    """Get Google Cloud credentials."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(
                    f"Missing {CLIENT_SECRETS_FILE}. Download it from the Google Cloud Console."
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def get_translate_client():
    """Get a thread-local translate client."""
    if not hasattr(_thread_local, 'client'):
        _thread_local.client = translate.Client(credentials=get_credentials())
    return _thread_local.client

# Improved regex patterns for better text extraction
# Pattern for standard localization entries: key:number "text"
pattern_standard = re.compile(r'^(\s*)([^#\s][^:]*:\d+\s*")(.*)(".*?)$')
# Pattern for entries without version numbers: key "text" 
pattern_simple = re.compile(r'^(\s*)([^#\s][^:]*\s*")(.*)(".*?)$')

def should_translate_text(text: str) -> bool:
    """Determine if text should be translated based on content."""
    if not text or len(text.strip()) < 2:
        return False
    
    # Skip if text is mostly placeholders/variables
    placeholder_ratio = (text.count('$') + text.count('[') + text.count('{')) / len(text)
    if placeholder_ratio > 0.3:
        return False
    
    # Skip pure HTML/formatting
    if text.strip().startswith('<') and text.strip().endswith('>'):
        return False
        
    # Skip if already German (rough heuristic)
    german_words = ['der', 'die', 'das', 'und', 'oder', 'mit', 'von', 'zu', 'in', 'auf', 'für', 'ein', 'eine']
    text_lower = text.lower()
    german_word_count = sum(1 for word in german_words if f' {word} ' in f' {text_lower} ')
    if german_word_count > 2:
        return False
    
    return True

def translate_text_safe(client, text: str, max_retries: int = 3) -> str:
    """Safely translate text with retries and error handling."""
    if shutdown_event.is_set():
        return text
        
    if not should_translate_text(text):
        return text
        
    for attempt in range(max_retries):
        if shutdown_event.is_set():
            return text
            
        try:
            result = client.translate(text, target_language='de', source_language='en')
            translated = result['translatedText']
            
            # Basic quality check - if translation is dramatically different length, keep original
            if len(translated) > len(text) * 3 or len(translated) < len(text) * 0.3:
                return text
                
            return translated
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                continue
            else:
                print(f"    Warning: Failed to translate '{text[:50]}...': {e}")
                return text
    
    return text

def translate_line(line: str) -> str:
    """Translate a single line of localization text."""
    client = get_translate_client()
    
    # Try standard pattern first (key:number "text")
    match = pattern_standard.match(line)
    if not match:
        # Try simple pattern (key "text")
        match = pattern_simple.match(line)
    
    if match:
        indent, prefix, text, suffix = match.groups()
        translated_text = translate_text_safe(client, text)
        return f"{indent}{prefix}{translated_text}{suffix}\n"
    
    # Handle header line conversion
    if line.strip() == 'l_english:' or line.strip() == '\ufeffl_english:':
        return line.replace('l_english', 'l_german')
    
    return line

def translate_file(src_dest_pair: Tuple[Path, Path]) -> Tuple[Path, bool, str]:
    """Translate one file and save it to the destination."""
    src_path, dest_path = src_dest_pair
    
    if shutdown_event.is_set():
        return src_path, False, "Cancelled due to shutdown"
    
    try:
        # Create destination directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read source file
        with src_path.open("r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        total_lines = len(lines)
        translated_lines = 0
        
        print(f"  Translating {src_path.name} ({total_lines} lines)...")

        # Translate lines
        translated = []
        for i, line in enumerate(lines, start=1):
            if shutdown_event.is_set():
                return src_path, False, f"Cancelled after {i}/{total_lines} lines"
                
            original_line = line
            translated_line = translate_line(line)
            
            if translated_line != original_line:
                translated_lines += 1
                
            translated.append(translated_line)
            
            # Progress reporting every 25 lines or at end
            if i % 25 == 0 or i == total_lines:
                print(f"    {src_path.name}: {i}/{total_lines} lines processed")

        # Write translated file only if not cancelled
        if not shutdown_event.is_set():
            with dest_path.open("w", encoding="utf-8-sig") as out:  # utf-8-sig adds BOM
                out.writelines(translated)
            
        return src_path, True, f"Completed: {translated_lines}/{total_lines} lines translated"
        
    except Exception as e:
        return src_path, False, f"Error: {str(e)}"

def translate_directory(src_dir: Path, dest_dir: Path, max_workers: int = 4):
    """Translate all .yml files within src_dir to dest_dir using multiple threads."""
    
    # Collect all files to translate
    files_to_translate = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".yml"):
                src_path = Path(root) / file
                rel = src_path.relative_to(src_dir)
                dest_path = dest_dir / rel
                dest_path = Path(
                    str(dest_path).replace("_l_english", "_l_german")
                )
                files_to_translate.append((src_path, dest_path))

    total = len(files_to_translate)
    print(f"Found {total} files to translate using {max_workers} threads.")
    
    if total == 0:
        print("No files found to translate.")
        return

    # Process files in parallel
    start_time = time.time()
    completed = 0
    failed = 0
    cancelled = 0
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(translate_file, file_pair): file_pair[0] 
                for file_pair in files_to_translate
            }
            
            # Process completed tasks as they finish
            for future in as_completed(future_to_file):
                if shutdown_event.is_set():
                    print("\n⚠️  Cancelling remaining tasks...")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                    
                src_path, success, message = future.result()
                completed += 1
                
                if "Cancelled" in message:
                    cancelled += 1
                    print(f"[{completed}/{total}] ⚠️  {src_path.name} - {message}")
                elif success:
                    print(f"[{completed}/{total}] ✓ {message}")
                else:
                    failed += 1
                    print(f"[{completed}/{total}] ✗ {src_path.name} - {message}")
                    
    except KeyboardInterrupt:
        print("\n🛑 Force interrupted!")
        shutdown_event.set()

    elapsed_time = time.time() - start_time
    
    if shutdown_event.is_set():
        print(f"\n⚠️  Translation interrupted after {elapsed_time:.2f} seconds")
        print(f"Processed: {completed}/{total} files")
        if cancelled > 0:
            print(f"Cancelled: {cancelled} files")
        if failed > 0:
            print(f"Failed: {failed} files")
        print("✅ Partial results have been saved")
    else:
        print(f"\n✅ Translation complete!")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"Successfully processed: {completed - failed - cancelled}/{total} files")
        if failed > 0:
            print(f"Failed: {failed} files")

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print('Usage: translate_directory_to_german_improved.py <english_dir> <german_dir> [max_workers]')
        print('  max_workers: Number of parallel threads (default: 4)')
        sys.exit(1)
    
    src_dir = Path(sys.argv[1])
    dest_dir = Path(sys.argv[2])
    max_workers = int(sys.argv[3]) if len(sys.argv) == 4 else 4
    
    if not src_dir.exists():
        print(f"Error: Source directory {src_dir} does not exist.")
        sys.exit(1)
    
    if max_workers < 1 or max_workers > 16:
        print("Error: max_workers must be between 1 and 16")
        sys.exit(1)
        
    translate_directory(src_dir, dest_dir, max_workers)