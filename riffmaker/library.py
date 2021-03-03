import json
from typing import Tuple

_data = {}


def load_data():
    """Load program data from the data directory"""
    fh_notes = open("data/notes.json", "rt")
    fh_scales = open("data/scales.json", "rt")
    _data["notes"] = json.load(fh_notes)
    _data["scales"] = json.load(fh_scales)
    fh_notes.close()
    fh_scales.close()


def get_scales() -> "list":
    return [scale["name"] for scale in _data["scales"]]


def get_modes(scale_input) -> "list":
    return _data["scales"][scale_input]["modes"]


def get_intervals(scale_input) -> "list":
    return _data["scales"][scale_input]["intervals"]


def create_full_notes_list() -> "list":
    """Returns the full list of available notes, with both sharp and flat enharmonics."""
    return [
        pair[0] if pair[0] == pair[1] else pair[0] + "/" + pair[1]
        for pair in _data["notes"]
    ]


def create_sharp_notes_list() -> "list":
    """Returns the list of available notes with sharp accidentals."""
    return [pair[0] for pair in _data["notes"]]


def create_flat_notes_list() -> "list":
    """Returns the list of available notes with flat accidentals."""
    return [pair[1] for pair in _data["notes"]]


def build_scale(scale: "int", key: "int", mode: "int") -> "list":
    """Create a list of available notes from which to build a riff."""
    # FIXME hardcoding sharp list until we fix the key selection
    notes = create_sharp_notes_list()
    intervals = get_intervals(scale)
    sl = len(notes)
    il = len(intervals)
    scale_notes = []
    for i in range(mode, mode + il):
        scale_notes.append(notes[key % sl])
        key += intervals[i % il]
    return scale_notes


def generate_riff(notes: "list", phrase: "str") -> Tuple["list", "list"]:
    """Maps the characters of a phrase to a list of notes"""

    if len(phrase) == 0:
        return

    phrase = phrase.upper()
    offset = ord("A")
    sl = len(notes)

    scale_degrees = []
    riff = []
    for c in list(phrase):
        scale_degree = (ord(c) - offset) % sl
        scale_degrees.append(scale_degree)
        riff.append(notes[scale_degree])

    return (riff, scale_degrees)