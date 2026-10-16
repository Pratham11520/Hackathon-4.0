"""Compare a face image with the stored CIIE face encodings."""

import argparse
import json
from pathlib import Path

import face_recognition
import numpy as np


DEFAULT_ENCODINGS_PATH = Path("GPAICIIEENC.json")


def load_known_encodings(encodings_path=DEFAULT_ENCODINGS_PATH):
    """Load named face encodings saved as JSON-compatible number lists."""
    with Path(encodings_path).open("r", encoding="utf-8") as json_file:
        stored_encodings = json.load(json_file)

    if not isinstance(stored_encodings, dict) or not stored_encodings:
        raise ValueError("The face-encodings file must contain a non-empty object.")

    names = list(stored_encodings)
    encodings = np.asarray([stored_encodings[name] for name in names], dtype=float)
    return names, encodings


def find_matching_face(image_path, encodings_path=DEFAULT_ENCODINGS_PATH, tolerance=0.6):
    """Return the closest matching name and distance, or (None, None)."""
    names, known_encodings = load_known_encodings(encodings_path)
    image = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(image)

    if not unknown_encodings:
        return None, None

    distances = face_recognition.face_distance(known_encodings, unknown_encodings[0])
    closest_index = int(np.argmin(distances))
    closest_distance = float(distances[closest_index])

    if closest_distance <= tolerance:
        return names[closest_index], closest_distance
    return None, closest_distance


def main():
    parser = argparse.ArgumentParser(
        description="Find the closest matching stored face for an image."
    )
    parser.add_argument("image", help="Path to an image containing one face.")
    parser.add_argument(
        "--encodings",
        default=DEFAULT_ENCODINGS_PATH,
        help="Path to the JSON file containing named face encodings.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.6,
        help="Maximum face-distance value accepted as a match (default: 0.6).",
    )
    args = parser.parse_args()

    name, distance = find_matching_face(args.image, args.encodings, args.tolerance)
    if name is None:
        if distance is None:
            print("No face was detected in the supplied image.")
        else:
            print(f"No match found (closest distance: {distance:.3f}).")
        return

    print(f"Match found: {name} (distance: {distance:.3f})")


if __name__ == "__main__":
    main()
