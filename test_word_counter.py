import pytest
from collections import Counter
from word_counter import (
    get_words,
    count_words,
    save_csv,
    load_stop_words,
    STOP_WORDS,
    WordCounter,
)

def test_get_words_lowercases():
    assert get_words("Hello World") == ["hello", "world"]

def test_get_words_punctuation():
    assert get_words("Hello, World!") == ["hello", "world"]

def test_get_words_empty():
    assert get_words("") == []

def test_get_words_apostrophe():
    assert get_words("don't") == ["don't"]

def test_get_words_drops_numbers():
    assert get_words("room 101") == ["room"]

def test_get_words_removes_urls():
    assert get_words("Check https://example.com/page now") == ["check", "now"]

def test_get_words_removes_emails():
    assert get_words("Email me at a.b@example.com today") == ["email", "me", "at", "today"]

def test_get_words_keeps_hyphenated():
    assert get_words("a well-known idea") == ["a", "well-known", "idea"]

def test_get_words_edge_apostrophes():
    assert get_words("'quoted' text") == ["quoted", "text"]

def test_count_words_counts():
    counter = count_words(["data", "data", "items"])
    assert counter["data"] == 2
    assert counter["items"] == 1

def test_count_words_skips_stop_words():
    counter = count_words(["the", "data"])
    assert "the" not in counter

def test_count_words_keeps_stop_words_when_asked():
    counter = count_words(["the", "the"], skip_stop_words=False)
    assert counter["the"] == 2

def test_count_words_skips_single_letters():
    counter = count_words(["k", "data"])
    assert "k" not in counter

def test_save_csv(tmp_path):
    out = tmp_path / "out.csv"
    save_csv(Counter({"data": 2, "items": 1}), str(out))
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "word,count"
    assert lines[1] == "data,2"
    assert lines[2] == "items,1"

def test_wordcounter_counts_text():
    wc = WordCounter()
    wc.load_text("Data data items")
    assert wc.total_words == 3
    assert wc.unique_words == 2
    assert wc.top(1) == [("data", 2)]

def test_wordcounter_skips_stop_words():
    wc = WordCounter()
    wc.load_text("the data and the items")
    assert wc.total_words == 5
    assert "the" not in wc.counter
    assert wc.unique_words == 2

def test_wordcounter_custom_stop_words():
    wc = WordCounter(stop_words={"data"})
    wc.load_text("data items the")
    assert "data" not in wc.counter
    assert wc.counter["the"] == 1

def test_wordcounter_empty():
    wc = WordCounter()
    wc.load_text("")
    assert wc.total_words == 0
    assert wc.unique_words == 0
    assert wc.top() == []

def test_wordcounter_report():
    wc = WordCounter()
    wc.load_text("data data items")
    lines = wc.report(2).splitlines()
    assert lines[0].startswith("Rank")
    assert "data" in lines[2]

def test_wordcounter_load_pdf_without_text(monkeypatch):
    monkeypatch.setattr("word_counter.extract_text", lambda pdf_file: "   ")
    wc = WordCounter()
    with pytest.raises(ValueError):
        wc.load_pdf("anything.pdf")

def test_load_stop_words(tmp_path):
    file = tmp_path / "stop.txt"
    file.write_text("The\nand\n\n  of  \n", encoding="utf-8")
    assert load_stop_words(str(file)) == {"the", "and", "of"}

def test_default_stop_words_loaded():
    assert "the" in STOP_WORDS

def test_wordcounter_keep_stop_words():
    wc = WordCounter(stop_words=set())
    wc.load_text("the the data")
    assert wc.counter["the"] == 2