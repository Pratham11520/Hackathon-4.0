"""Persist word frequencies in a JSON file."""

import json
from collections import defaultdict
from pathlib import Path


def load_word_frequencies(file_name):
    """Load a frequency mapping, validating existing JSON data."""
    path = Path(file_name)
    if not path.exists() or path.stat().st_size == 0:
        return defaultdict(int)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error.msg}") from error

    if not isinstance(data, dict):
        raise ValueError("Word-frequency data must be a JSON object.")

    frequencies = defaultdict(int)
    for word, count in data.items():
        if not isinstance(word, str) or not isinstance(count, int) or count < 0:
            raise ValueError("Word frequencies must map strings to non-negative integers.")
        frequencies[word] = count
    return frequencies


def store_new_words(new_words, file_name):
    """Add words to the frequency mapping and save it atomically."""
    path = Path(file_name)
    frequencies = load_word_frequencies(path)

    for word in new_words:
        if not isinstance(word, str):
            raise ValueError("Each stored word must be a string.")
        frequencies[word] += 1

    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(dict(frequencies), file, indent=4, sort_keys=True)
        file.write("\n")
    temporary_path.replace(path)

    return dict(frequencies)
