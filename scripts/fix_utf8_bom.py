#!/usr/bin/env python3
"""
Fix UTF-8 BOM encoding for existing German localization files.
Hearts of Iron IV requires UTF-8 BOM for all localization files.
"""

import os
from pathlib import Path
import sys

def has_bom(file_path: Path) -> bool:
    """Check if file has UTF-8 BOM."""
    try:
        with file_path.open("rb") as f:
            return f.read(3) == b'\xef\xbb\xbf'
    except Exception:
        return False

def add_bom_to_file(file_path: Path) -> bool:
    """Add UTF-8 BOM to file if it doesn't have one."""
    if has_bom(file_path):
        return False  # Already has BOM
    
    try:
        # Read content without BOM
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Write back with BOM
        with file_path.open("w", encoding="utf-8-sig") as f:
            f.write(content)
        
        return True  # BOM added
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_german_localization_files(base_dir: Path):
    """Fix UTF-8 BOM for all German localization files."""
    german_dir = base_dir / "localisation" / "german"
    
    if not german_dir.exists():
        print(f"❌ German localization directory not found: {german_dir}")
        return
    
    print(f"🔍 Scanning German localization files in: {german_dir}")
    
    yml_files = list(german_dir.glob("**/*.yml"))
    if not yml_files:
        print("❌ No .yml files found in German localization directory")
        return
    
    print(f"📁 Found {len(yml_files)} German localization files")
    
    fixed_count = 0
    already_ok_count = 0
    error_count = 0
    
    for yml_file in yml_files:
        print(f"  Checking: {yml_file.name}")
        
        if has_bom(yml_file):
            already_ok_count += 1
            print(f"    ✅ Already has BOM")
        else:
            if add_bom_to_file(yml_file):
                fixed_count += 1
                print(f"    🔧 Fixed - BOM added")
            else:
                error_count += 1
                print(f"    ❌ Failed to fix")
    
    print(f"\n📊 Results:")
    print(f"  ✅ Already correct: {already_ok_count}")
    print(f"  🔧 Fixed: {fixed_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📁 Total: {len(yml_files)}")
    
    if fixed_count > 0:
        print(f"\n🎉 Successfully fixed {fixed_count} files!")
        print("   You can now restart Hearts of Iron IV and the German translations should load correctly.")
    elif already_ok_count == len(yml_files):
        print(f"\n✅ All files were already correct!")
    else:
        print(f"\n⚠️  Some files could not be fixed. Check file permissions.")

def main():
    """Main function."""
    print("=" * 60)
    print("UTF-8 BOM FIX FOR HEARTS OF IRON IV LOCALIZATION")
    print("=" * 60)
    print()
    
    # Get base directory (should be the mod root)
    if len(sys.argv) > 1:
        base_dir = Path(sys.argv[1])
    else:
        base_dir = Path.cwd()
    
    if not base_dir.exists():
        print(f"❌ Directory does not exist: {base_dir}")
        sys.exit(1)
    
    # Check if this looks like the right directory
    if not (base_dir / "localisation").exists():
        print(f"❌ This doesn't look like a Hearts of Iron IV mod directory.")
        print(f"   Expected to find 'localisation' folder in: {base_dir}")
        print(f"   Usage: python fix_utf8_bom.py [mod_directory]")
        sys.exit(1)
    
    fix_german_localization_files(base_dir)

if __name__ == "__main__":
    main()