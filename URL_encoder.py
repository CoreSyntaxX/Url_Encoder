#!/usr/bin/env python3

import urllib.parse
import pyperclip
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

PYRAMID = f"""
{Fore.YELLOW}
       /\\
      /  \\
     / /\\ \\
    / ____ \\
   /_/    \\_\\
{Fore.CYAN}
"""

TOOL_NAME = f"""
{Fore.CYAN}=========================================
     🔗 {Fore.YELLOW}URL ENCODER / DECODER TOOL
         {Fore.MAGENTA}by CoreSytaxX
{Fore.CYAN}=========================================
"""

CHEAT_SHEET = f"""
{Fore.GREEN}===== URL Encoding Cheat Sheet =====

{Fore.YELLOW} Character     Encoded
 ----------    --------
   Space         %20
   "             %22
   #             %23
   %             %25
   &             %26
   '             %27
   (             %28
   )             %29
   +             %2B
   ,             %2C
   /             %2F
   :             %3A
   ;             %3B
   <             %3C
   =             %3D
   >             %3E
   ?             %3F
   @             %40
"""

LOG_FILE = "url_tool_log.txt"

def log_result(action, original, result):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {action}\n")
        f.write(f"Original: {original}\nResult:   {result}\n\n")

def encode_url(text):
    return urllib.parse.quote(text, safe=':/?&=#')

def decode_url(text):
    return urllib.parse.unquote(text)

def auto_detect(text):
    """Detect if string contains URL encoding"""
    return '%' in text and any(c.isalpha() for c in text)

def process_file(path, mode):
    if not os.path.exists(path):
        print(f"{Fore.RED}❌ File not found: {path}")
        return

    print(f"{Fore.CYAN}📄 Processing file: {path}")
    with open(path, "r") as f:
        lines = f.readlines()

    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        result = decode_url(line) if mode == "decode" else encode_url(line)
        results.append((line, result))
        log_result(mode.upper(), line, result)

    output_file = "processed_output.txt"
    with open(output_file, "w") as f:
        for _, result in results:
            f.write(f"{result}\n")

    print(f"{Fore.GREEN}✅ Processed {len(results)} lines. Output saved to {output_file}.")

def main_menu():
    print(PYRAMID)
    print(TOOL_NAME)

    while True:
        print(f"""{Fore.CYAN}Choose an option:
  {Fore.YELLOW}1. Encode URL or Text
  2. Decode Encoded URL
  3. Auto-Detect & Handle (Encode/Decode)
  4. Batch Process File
  5. Show URL Encoding Cheat Sheet
  6. Exit""")

        choice = input(f"{Fore.CYAN}Enter option number (1-6): ").strip()

        if choice == "1":
            text = input("Enter text or URL to encode: ")
            result = encode_url(text)
            pyperclip.copy(result)
            print(f"\n{Fore.GREEN}✅ Encoded Result:\n{result}")
            print(f"{Fore.MAGENTA}(Copied to clipboard)\n")
            log_result("ENCODE", text, result)

        elif choice == "2":
            text = input("Enter encoded URL to decode: ")
            result = decode_url(text)
            pyperclip.copy(result)
            print(f"\n{Fore.GREEN}✅ Decoded Result:\n{result}")
            print(f"{Fore.MAGENTA}(Copied to clipboard)\n")
            log_result("DECODE", text, result)

        elif choice == "3":
            text = input("Enter input to auto-detect and process: ")
            if auto_detect(text):
                result = decode_url(text)
                action = "Auto-DECODE"
            else:
                result = encode_url(text)
                action = "Auto-ENCODE"
            pyperclip.copy(result)
            print(f"\n{Fore.GREEN}✅ {action} Result:\n{result}")
            print(f"{Fore.MAGENTA}(Copied to clipboard)\n")
            log_result(action, text, result)

        elif choice == "4":
            path = input("Enter path to text file with URLs (one per line): ").strip()
            mode = input("Choose mode (encode/decode): ").strip().lower()
            if mode in ("encode", "decode"):
                process_file(path, mode)
            else:
                print(f"{Fore.RED}Invalid mode. Use 'encode' or 'decode'.\n")

        elif choice == "5":
            print(CHEAT_SHEET)

        elif choice == "6":
            print(f"{Fore.YELLOW}👋 Exiting... Goodbye!")
            sys.exit(0)

        else:
            print(f"{Fore.RED}⚠️ Invalid choice. Please enter a number between 1 and 6.\n")

if __name__ == "__main__":
    main_menu()

