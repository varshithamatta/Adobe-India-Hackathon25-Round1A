# PDF Outline Extractor - Adobe India Hackathon 2025

## Overview

This solution extracts the **title** and hierarchical **headings (H1, H2, H3)** from PDF documents by analyzing font size and style information. It uses heuristic rules to distinguish headings from body text and filters out common non-heading labels, providing a structured outline of your PDFs.

The workflow is fully automated: all PDF files placed in the `/input` folder will be processed, and the corresponding JSON output files with extracted outlines will be saved in the `/output` folder.

## Approach

- Uses `pdfminer.six` to parse PDFs and extract text with font size and style metadata.
- Headings identified based on relative font size (larger than common body text) and boldness.
- The largest text on the first page is extracted as the document **title**.
- Filters out typical form field labels and very short text that are unlikely to be headings.
- Processes all PDFs in batch, writing one JSON outline file per PDF.

## Libraries Used

- [`pdfminer.six`](https://pdfminersix.readthedocs.io/en/latest/) (version 20221105): For PDF text extraction and font metadata.

## Files

- `index.py` — Main script scanning `/input` folder and calling `extractor.py` on each PDF.
- `extractor.py` — Extracts title and heading outlines from a single PDF.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — Container definition for easy build and run.

## How to Build and Run

### Build Docker Image

Make sure `index.py`, `extractor.py`, `requirements.txt`, and `Dockerfile` are in the same directory. Then build the Docker image:

`docker build -t pdf-outline-extractor .`


### Run Container for Batch Processing

Mount your local `input` and `output` directories and run the container:

`docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor`

- Put all your PDFs inside the `input/` folder.
- Extracted outlines will appear as JSON files in `output/`, sharing the same base filename as the source PDFs.
