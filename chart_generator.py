"""Generate a pie chart from a JSON word-frequency mapping."""

import json
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_DATA_PATH = Path("new_words.json")


def load_word_frequencies(data_path=DEFAULT_DATA_PATH):
    """Return validated word-frequency data, or an empty mapping when absent."""
    path = Path(data_path)
    if not path.exists() or path.stat().st_size == 0:
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error.msg}") from error

    if not isinstance(data, dict):
        raise ValueError("Word-frequency data must be a JSON object.")

    frequencies = {}
    for word, value in data.items():
        if not isinstance(word, str) or not isinstance(value, (int, float)):
            raise ValueError("Each word must have a numeric frequency.")
        if value < 0:
            raise ValueError("Word frequencies cannot be negative.")
        frequencies[word] = value

    if frequencies and sum(frequencies.values()) == 0:
        raise ValueError("At least one word frequency must be greater than zero.")
    return frequencies


def generate_chart(data_path=DEFAULT_DATA_PATH, show=True):
    """Create a word-frequency pie chart and return its figure and axes."""
    data = load_word_frequencies(data_path)
    if not data:
        print("No data available.")
        return None, None

    figure, axes = plt.subplots()
    axes.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
    axes.set_title("Word Frequencies")
    axes.axis("equal")

    if show:
        plt.show()
    return figure, axes


if __name__ == "__main__":
    generate_chart()
