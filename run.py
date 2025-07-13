#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    print("🚀 Starting Photo Upload Gallery...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("📸 Opening http://localhost:5001 in your browser...")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask application
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have Flask installed: pip3 install -r requirements.txt")

if __name__ == "__main__":
    main() 