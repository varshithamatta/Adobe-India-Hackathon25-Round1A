# index.py
"""
Adobe India Hackathon 2024 - Script to Process All PDFs in input/
----------------------------------------------------------------------------
Scans input/ for PDF files, sends each to extractor.py.
Writes JSONs to output/, with same base filename as PDF.

Author: [Your Name]
"""
import os
import subprocess

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if fname.lower().endswith('.pdf'):
            inpath = os.path.join(INPUT_DIR, fname)
            outfname = fname.rsplit('.', 1)[0] + '.json'
            outpath = os.path.join(OUTPUT_DIR, outfname)
            print(f"Processing: {inpath}")
            ret = subprocess.run(['python', 'extractor.py', inpath, outpath])
            if ret.returncode != 0:
                print(f"Failed: {inpath}")

if __name__ == '__main__':
    main()
