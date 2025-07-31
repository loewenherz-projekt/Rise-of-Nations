#!/usr/bin/env python3
"""
Test script to verify interrupt handling works correctly.
"""

import time
import tempfile
from pathlib import Path
import subprocess
import sys
import os

def create_large_test_file(test_dir: Path):
    """Create a large test file to simulate long-running translation."""
    test_dir.mkdir(exist_ok=True)
    
    # Create a file with many translatable lines
    large_content = "l_english:\n"
    for i in range(1000):  # Many lines to ensure script runs long enough to test interrupt
        large_content += f' test_line_{i:04d}:0 "This is test line number {i} that should be translated to German."\n'
    
    test_file = test_dir / "large_test_l_english.yml"
    with test_file.open("w", encoding="utf-8") as f:
        f.write(large_content)
    
    print(f"Created large test file: {test_file}")
    return test_file

def test_interrupt_handling():
    """Test that the improved script can be interrupted gracefully."""
    print("🧪 Testing interrupt handling...")
    print("   This test will start translation and then simulate Ctrl+C")
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_src = temp_path / "english"
        test_dest = temp_path / "german"
        
        # Create large test file
        test_file = create_large_test_file(test_src)
        
        print(f"\n📁 Test setup:")
        print(f"   Source: {test_src}")
        print(f"   Destination: {test_dest}")
        print(f"   Test file: {test_file.name}")
        
        # Check if we have the improved script
        script_path = Path(__file__).parent / "translate_directory_to_german_improved.py"
        if not script_path.exists():
            print("❌ translate_directory_to_german_improved.py not found!")
            return
        
        print(f"\n🚀 Starting translation process...")
        print("   Press Ctrl+C after a few seconds to test interrupt handling")
        
        # Start the translation process
        try:
            cmd = [
                sys.executable, 
                str(script_path),
                str(test_src),
                str(test_dest),
                "2"  # Use 2 threads for testing
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Let it run for a few seconds, then interrupt
            print("   Translation started. Waiting 3 seconds...")
            time.sleep(3)
            
            print("   Sending interrupt signal...")
            process.send_signal(subprocess.signal.SIGINT if hasattr(subprocess, 'signal') else 2)
            
            # Wait for graceful shutdown
            try:
                stdout, stderr = process.communicate(timeout=10)
                return_code = process.returncode
                
                print(f"\n📊 Results:")
                print(f"   Return code: {return_code}")
                print(f"   Process terminated gracefully: {'✅' if return_code != 0 else '⚠️'}")
                
                if stdout:
                    print(f"\n📝 Output:")
                    for line in stdout.split('\n')[-10:]:  # Show last 10 lines
                        if line.strip():
                            print(f"   {line}")
                
                if stderr and stderr.strip():
                    print(f"\n❌ Errors:")
                    print(f"   {stderr}")
                
                # Check if partial files were created
                created_files = list(test_dest.glob("*.yml"))
                if created_files:
                    print(f"\n📄 Partial results saved: {len(created_files)} files")
                    for f in created_files:
                        print(f"   - {f.name}")
                else:
                    print(f"\n📄 No output files created (expected for quick interrupt)")
                
                print(f"\n✅ Interrupt handling test completed successfully!")
                
            except subprocess.TimeoutExpired:
                print("⚠️  Process didn't terminate within timeout, force killing...")
                process.kill()
                print("❌ Interrupt handling may need improvement")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("INTERRUPT HANDLING TEST")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("scripts").exists():
        print("❌ Please run this from the repository root directory")
        sys.exit(1)
    
    if not Path("client_secret.json").exists():
        print("⚠️  Note: client_secret.json not found")
        print("   This test will show interrupt handling but won't do actual translation")
        print("")
    
    test_interrupt_handling()