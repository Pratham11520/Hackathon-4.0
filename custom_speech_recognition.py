"""Recognize speech and map configured keyword groups to responses."""

import json
from pathlib import Path

import speech_recognition as sr


def load_responses(responses_file):
    """Load and validate the keyword-to-response mapping."""
    path = Path(responses_file)
    try:
        with path.open("r", encoding="utf-8") as file:
            responses = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Responses file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error.msg}") from error

    if not isinstance(responses, dict):
        raise ValueError("Responses must be a JSON object of keyword groups and values.")
    return responses


def speech_recognition(
    responses_file,
    timeout=None,
    phrase_time_limit=None,
    max_attempts=None,
):
    """Listen for a matching response, returning None when no match is found.

    The max_attempts argument is optional; omit it to preserve continuous listening.
    """
    responses = load_responses(responses_file)
    recognizer = sr.Recognizer()
    attempts = 0

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while max_attempts is None or attempts < max_attempts:
            try:
                audio = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
            except sr.WaitTimeoutError:
                attempts += 1
                print("Listening timed out.")
                continue

            attempts += 1
            try:
                text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("I didn't understand that.")
                continue
            except sr.RequestError as error:
                print("Speech recognition service error:", error)
                return None

            print("Recognized:", text)
            normalized_text = text.casefold()
            for word_group, response in responses.items():
                keywords = str(word_group).casefold().split()
                if any(keyword in normalized_text for keyword in keywords):
                    return response

            print("I didn't understand that.")

    return None
