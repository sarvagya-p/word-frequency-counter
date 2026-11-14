import os
import re
from collections import Counter
from pypdf import PdfReader

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
    """Return a list of lowercase words from a block of text."""
    return re.findall(r"[a-z']+", text.lower())


def count_words(words, skip_stop_words=True):
    """Count how often each word appears."""
    if skip_stop_words:
        words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    return Counter(words)


def show_top(counter, n=5):
    print(f"{'Rank':<6}{'Word':<12}{'Count':<6}")
    print("-" * 24)
    for rank, (word, count) in enumerate(counter.most_common(n), start=1):
        print(f"{rank:<6}{word:<12}{count:<6}")


if __name__ == "__main__":
    while True:
        pdf_file = input("PDF file name (or press Enter to quit): ").strip()

        if pdf_file == "":
            break

        if not os.path.exists(pdf_file):
            print(f"File not found: {pdf_file}")
        else:
            text = extract_text(pdf_file)
            if not text.strip():
                print("No text could be extracted from this PDF.")
            else:
                words = get_words(text)
                counter = count_words(words)
                print(f"Total words: {len(words)}")
                print(f"Unique words (after removing stop words): {len(counter)}\n")
                show_top(counter, n=5)
                break