from word_counter import get_words, count_words

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