import csv
import os
import re
import sys
from collections import Counter
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# Common words we usually don't care about
STOP_WORDS = {
    "the", "is", "of", "and", "to", "a", "in", "it", "with", "you",
    "what", "that", "may", "this", "are", "for", "be", "as", "on", "by",
    "or", "can", "not", "an", "if", "we", "from", "have", "has", "at",
    "will", "which", "each", "all", "was", "were", "but", "so", "do",
}

def extract_text(pdf_file, save_as="output2.txt"):
    """Extract text from every page of a PDF and save it to a txt file."""
    reader = PdfReader(pdf_file)
    all_text = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            all_text += txt + "\n\n"
    with open(save_as, "w", encoding="utf-8") as f:
        f.write(all_text)
    return all_text

def get_words(text):
    """Return a list of lowercase words from a block of text.

    URLs and email addresses are removed first. Words may contain an
    apostrophe or hyphen inside them (don't, well-known).
    """
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    return re.findall(r"[a-z]+(?:['-][a-z]+)*", text)

def count_words(words, skip_stop_words=True, stop_words=None):
    """Count how often each word appears."""
    if stop_words is None:
        stop_words = STOP_WORDS
    if skip_stop_words:
        words = [w for w in words if w not in stop_words and len(w) > 1]
    return Counter(words)

def save_csv(counter, filename="results.csv"):
    """Save every word and its count to a CSV file, most common first."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word", "count"])
        for word, count in counter.most_common():
            writer.writerow([word, count])

class WordCounter:
    """Holds the words from one document and how often each appears."""

    def __init__(self, stop_words=None):
        self.stop_words = STOP_WORDS if stop_words is None else set(stop_words)
        self.words = []
        self.counter = Counter()

    def load_text(self, text):
        """Split a block of text into words and count them."""
        self.words = get_words(text)
        self.counter = count_words(self.words, stop_words=self.stop_words)

    def load_pdf(self, pdf_file):
        """Extract the text of a PDF and count its words."""
        text = extract_text(pdf_file)
        if not text.strip():
            raise ValueError("No text could be extracted from this PDF.")
        self.load_text(text)

    @property
    def total_words(self):
        return len(self.words)

    @property
    def unique_words(self):
        return len(self.counter)

    def top(self, n=5):
        """Return the n most common words as (word, count) pairs."""
        return self.counter.most_common(n)

    def report(self, n=5):
        """Return a ranked table of the n most common words as text."""
        lines = [f"{'Rank':<6}{'Word':<12}{'Count':<6}", "-" * 24]
        for rank, (word, count) in enumerate(self.top(n), start=1):
            lines.append(f"{rank:<6}{word:<12}{count:<6}")
        return "\n".join(lines)

    def __str__(self):
        return self.report()

def analyze(pdf_file):
    """Analyze one PDF. Return True if it worked, False if something went wrong."""
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        return False

    wc = WordCounter()
    try:
        wc.load_pdf(pdf_file)
    except PdfReadError:
        print(f"Could not read {pdf_file}: it may be corrupted or password-protected.")
        return False
    except ValueError as error:
        print(error)
        return False

    print(f"Total words: {wc.total_words}")
    print(f"Unique words (after removing stop words): {wc.unique_words}\n")
    print(wc)
    save_csv(wc.counter)
    print("\nSaved all word counts to results.csv")
    return True

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if not analyze(sys.argv[1]):
            sys.exit(1)
    elif len(sys.argv) == 1:
        while True:
            pdf_file = input("PDF file name (or press Enter to quit): ").strip()
            if pdf_file == "":
                break
            if analyze(pdf_file):
                break
    else:
        sys.exit("Usage: python word_counter.py [file.pdf]")