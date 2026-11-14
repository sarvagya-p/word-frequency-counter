# word-frequency-counter

A Python program that extracts text from a PDF and shows the most frequently used words.

## How it works
1. Reads every page of a PDF with `pypdf` and saves the text to `output2.txt`
2. Cleans the text into lowercase words using a regular expression
3. Removes common stop words (like "the", "is", "of")
4. Counts words with `collections.Counter` and prints a ranked table

## Run it
```
pip install -r requirements.txt
python word_counter.py
```

By default it reads `sample.pdf` from the same folder. `sample.pdf` is a short four-page reading on how recommendation systems work, included so the program runs out of the box. To analyze your own document, replace it with any text-based PDF and update the file name in `word_counter.py`.

## Sample output
```
Total words: 1237
Unique words (after removing stop words): 508

Rank  Word        Count
------------------------
1     data        11
2     items       9
3     useful      8
4     first       7
5     relevant    7
```

## Known limitations
- Headers and footers that repeat on every page are counted each time.
- Scanned PDFs (images of text) won't work, since there is no text to extract.

## Roadmap
Planned upgrades as I work through CS50P: error handling for missing files, passing the PDF name as an argument, unit tests, saving results to CSV.
- Lecture 1: handles a missing or empty PDF with clear messages
- Lecture 2: re-prompt until a valid PDF is given

## About
Part of my CS50P learning journey: [learning-log](https://github.com/sarvagya-p/learning-log)