# extractor.py
"""
Adobe India Hackathon 2024 - "Connecting the Dots" PDF Outline Extractor
----------------------------------------------------------------------------
Extracts the title and headings (H1, H2, H3) from a PDF using font size and style.

Features:
- Headings extracted based on relative font size (larger than body text).
- Filters out common non-heading texts (numbers, form fields, short text).
- Title extracted from largest text blocks on first page.

Usage:
    python extractor.py input.pdf output.json

Author: [Your Name]
"""

import sys
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine

# Minimum heading length (exclude very short items)
MIN_HEADING_LENGTH = 4

# Common form-like field labels to exclude from headings
COMMON_FIELD_NAMES = {
    "name", "date", "amount", "id", "address", "dob", "number", "signature",
    "total", "mrn", "remarks", "score", "grade", "code", "ref", "phone"
}

def is_probable_heading(text, fontsize, body_fontsize):
    txt = text.strip()
    if len(txt) < MIN_HEADING_LENGTH:
        return False
    if txt.isdigit():
        return False
    if txt.lower() in COMMON_FIELD_NAMES:
        return False
    # Heading font size should be larger than the body text font size
    if fontsize <= body_fontsize:
        return False
    return True

def extract_title_and_headings(pdf_path):
    headings = []
    font_stats = {}
    segments = []

    # Extract text segments with font info from all pages
    for page_num, page_layout in enumerate(extract_pages(pdf_path), 1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if not isinstance(text_line, LTTextLine):
                        continue
                    run_text = ""
                    run_size = None
                    run_bold = None
                    fontnames = []
                    segs = []
                    for char in text_line:
                        if isinstance(char, LTChar):
                            char_size = round(char.size, 2)
                            char_bold = ('Bold' in char.fontname or 'bold' in char.fontname or 'BD' in char.fontname)
                            char_fontname = char.fontname

                            if run_size is None:
                                run_size = char_size
                                run_bold = char_bold
                                fontnames = [char_fontname]
                                run_text = char.get_text()
                            elif (run_size == char_size) and (run_bold == char_bold):
                                run_text += char.get_text()
                                fontnames.append(char_fontname)
                            else:
                                text_piece = run_text.strip()
                                if text_piece:
                                    segs.append({
                                        'text': text_piece,
                                        'fontsize': run_size,
                                        'is_bold': run_bold,
                                        'page': page_num
                                    })
                                    font_stats.setdefault(run_size, 0)
                                    font_stats[run_size] += 1
                                run_size = char_size
                                run_bold = char_bold
                                fontnames = [char_fontname]
                                run_text = char.get_text()
                    # Last run of the line
                    if run_text.strip():
                        segs.append({
                            'text': run_text.strip(),
                            'fontsize': run_size,
                            'is_bold': run_bold,
                            'page': page_num
                        })
                        font_stats.setdefault(run_size, 0)
                        font_stats[run_size] += 1
                    segments.extend(segs)

    if not font_stats:
        # No text found: return empty result
        return {"title": "", "outline": []}

    # Find the most common font size (likely body text)
    most_common_fontsize = max(font_stats.items(), key=lambda x: x[1])[0]

    # Sort font sizes descending order - largest are headings/titles
    font_sizes_sorted = sorted(font_stats.keys(), reverse=True)
    levels = ['H1', 'H2', 'H3']
    level_map = {}
    for i, fz in enumerate(font_sizes_sorted[:len(levels)]):
        level_map[fz] = levels[i]

    # Extract title: biggest font size on first page
    title_candidates = [s for s in segments if s['page'] == 1 and s['fontsize'] == font_sizes_sorted[0]]
    title_lines = [s['text'] for s in title_candidates]
    title = ' '.join(title_lines).strip() if title_lines else ""


    import re
    def normalize_text(s):
        # Lowercase, remove punctuation, collapse whitespace
        return re.sub(r'\W+', ' ', s).strip().lower()

    title_normalized = normalize_text(title)
    title_words = set(title_normalized.split())

    # Build headings list with filtering
    for seg in segments:
        level = level_map.get(seg['fontsize'])
        text_clean = seg['text'].strip()
        heading_normalized = normalize_text(text_clean)
        heading_words = set(heading_normalized.split())
        if level and is_probable_heading(text_clean, seg['fontsize'], most_common_fontsize):
            # Exclude if heading is the same as the title
            if heading_normalized == title_normalized:
                continue
            # Exclude if all title words are present in heading (regardless of order or extra words)
            if title_words and title_words.issubset(heading_words):
                continue
            # Exclude if heading is a significant word/phrase from the title
            if heading_normalized in title_normalized or title_normalized in heading_normalized:
                continue
            headings.append({'level': level, 'text': text_clean, 'page': seg['page']})

    return {
        "title": title,
        "outline": headings
    }

def main():
    if len(sys.argv) != 3:
        print("Usage: python extractor.py input.pdf output.json")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    outline = extract_title_and_headings(pdf_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
