# word-frequency-counter

A Python program that extracts text from a PDF and shows the most frequently used words.

## How it works
1. Takes a PDF file name from the command line (or asks for one if you don't give it)
2. Reads every page of the PDF with `pypdf` and saves the text to `output2.txt`
3. Cleans the text into lowercase words using a regular expression
4. Removes common stop words (like "the", "is", "of") and single letters
5. Counts words with `collections.Counter` and prints a ranked table

## Run it
```
pip install -r requirements.txt
python word_counter.py sample.pdf
```
If you run it without a file name, it asks for one, and you can press Enter to quit.

`sample.pdf` is a short four-page reading on how recommendation systems work, included so the program runs out of the box. To analyze your own document, put any text-based PDF in this folder and pass its name.

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
## Use it in Python
```python
from word_counter import WordCounter

wc = WordCounter()
wc.load_pdf("sample.pdf")
print(wc.top(3))
```

## Run the tests
```
pip install -r requirements-dev.txt
python -m pytest
```

## Known limitations
- Headers and footers that repeat on every page are counted each time.
- Scanned PDFs (images of text) won't work, since there is no text to extract.

## Progress
- Lecture 1: handles a missing or empty PDF with clear messages
- Lecture 2: re-prompt until a valid PDF is given
- Lecture 3: handles unreadable or corrupted PDFs with try/except
- Lecture 4: takes the PDF name from the command line with sys.argv
- Lecture 5: unit tests for word cleaning and counting with pytest
- Lecture 6: saves all word counts to a CSV file
- Lecture 7: cleans text with regular expressions (removes URLs and emails, keeps hyphenated words)
- Lecture 8: refactored into a WordCounter class with methods and properties

## Roadmap
Planned upgrades as I work through CS50P: error handling for missing files, passing the PDF name as an argument, saving results to CSV.

## About
Part of my CS50P learning journey: [learning-log](https://github.com/sarvagya-p/learning-log)