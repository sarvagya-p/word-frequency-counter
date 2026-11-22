import argparse
import csv
import os
import re
import sys
from collections import Counter

from pypdf import PdfReader
from pypdf.errors import PdfReadError

STOPWORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stopwords.txt")

def load_stop_words(path: str = STOPWORDS_FILE) -> set[str]:
    """Read stop words from a text file, one word per line."""
    with open(path, encoding="utf-8") as file:
        return {line.strip().lower() for line in file if line.strip()}

STOP_WORDS = load_stop_words()

def extract_text(pdf_file: str, save_as: str = "output2.txt") -> str:
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

def get_words(text: str) -> list[str]:
    """Return a list of lowercase words from a block of text.

    URLs and email addresses are removed first. Words may contain an
    apostrophe or hyphen inside them (don't, well-known).
    """
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    return re.findall(r"[a-z]+(?:['-][a-z]+)*", text)

def count_words(
    words: list[str],
    skip_stop_words: bool = True,
    stop_words: set[str] | None = None,
) -> Counter:
    """Count how often each word appears."""
    if stop_words is None:
        stop_words = STOP_WORDS
    if skip_stop_words:
        words = [w for w in words if w not in stop_words and len(w) > 1]
    return Counter(words)

def save_csv(counter: Counter, filename: str = "results.csv") -> None:
    """Save every word and its count to a CSV file, most common first."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word", "count"])
        for word, count in counter.most_common():
            writer.writerow([word, count])

class WordCounter:
    """Holds the words from one document and how often each appears."""

    def __init__(self, stop_words: set[str] | None = None) -> None:
        self.stop_words = STOP_WORDS if stop_words is None else set(stop_words)
        self.words: list[str] = []
        self.counter: Counter = Counter()

    def load_text(self, text: str) -> None:
        """Split a block of text into words and count them."""
        self.words = get_words(text)
        self.counter = count_words(self.words, stop_words=self.stop_words)

    def load_pdf(self, pdf_file: str) -> None:
        """Extract the text of a PDF and count its words."""
        text = extract_text(pdf_file)
        if not text.strip():
            raise ValueError("No text could be extracted from this PDF.")
        self.load_text(text)

    @property
    def total_words(self) -> int:
        return len(self.words)

    @property
    def unique_words(self) -> int:
        return len(self.counter)

    def top(self, n: int = 5) -> list[tuple[str, int]]:
        """Return the n most common words as (word, count) pairs."""
        return self.counter.most_common(n)

    def report(self, n: int = 5) -> str:
        """Return a ranked table of the n most common words as text."""
        lines = [f"{'Rank':<6}{'Word':<12}{'Count':<6}", "-" * 24]
        for rank, (word, count) in enumerate(self.top(n), start=1):
            lines.append(f"{rank:<6}{word:<12}{count:<6}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.report()

def analyze(pdf_file: str, top: int = 5, keep_stop_words: bool = False) -> bool:
    """Analyze one PDF. Return True if it worked, False if something went wrong."""
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        return False

    wc = WordCounter(stop_words=set() if keep_stop_words else None)
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
    print(wc.report(top))
    save_csv(wc.counter)
    print("\nSaved all word counts to results.csv")
    return True

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line options."""
    parser = argparse.ArgumentParser(
        description="Show the most frequently used words in a PDF."
    )
    parser.add_argument("file", nargs="?", help="PDF to analyze (asks if left out)")
    parser.add_argument(
        "-n", "--top", type=int, default=5, help="how many top words to show (default 5)"
    )
    parser.add_argument(
        "--keep-stop-words",
        action="store_true",
        help="count common words like 'the' too",
    )
    return parser.parse_args(argv)

def main() -> None:
    args = parse_args()
    if args.top < 1:
        sys.exit("--top must be at least 1")

    if args.file:
        if not analyze(args.file, args.top, args.keep_stop_words):
            sys.exit(1)
    else:
        while True:
            pdf_file = input("PDF file name (or press Enter to quit): ").strip()
            if pdf_file == "":
                break
            if analyze(pdf_file, args.top, args.keep_stop_words):
                break

if __name__ == "__main__":
    main()