import sys, signal
import json

data = {}

def exit_handler(signal, frame):
    print('\n\nInterrupt received, shutting down')
    sys.exit(0)

def load_data():
    """Load program data from the data directory"""
    fh_notes = open('data/notes.json', 'rt')
    fh_scales = open('data/scales.json', 'rt')
    data['notes'] = json.load(fh_notes)
    data['scales'] = json.load(fh_scales)
    fh_notes.close()
    fh_scales.close()

def create_full_notes_list() -> 'list':
    """Returns the full list of available notes, with both sharp and flat enharmonics."""
    return [pair[0] if pair[0] == pair[1] else pair[0]+'/'+pair[1] for pair in data['notes']]

def create_sharp_notes_list() -> 'list':
    """Returns the list of available notes with sharp accidentals."""
    return [pair[0] for pair in data['notes']]

def create_flat_notes_list() -> 'list':
    """Returns the list of available notes with flat accidentals."""
    return [pair[1] for pair in data['notes']]

def build_scale() -> 'list':
    """Create a list of available notes from which to build a riff."""

    scales = [scale['name'] for scale in data['scales']]
    print('\nThe following scales are available:\n')
    for i, scale in enumerate(scales, start=1):
        print('{}. {}'.format(i, scale))
    # decrement by one for index lookup
    scale_input = int(input('\nSelect a scale: '))-1

    # TODO allow users to switch between sharps and flats
    keys = create_full_notes_list()
    print('\nThe following keys are available:\n')
    for i, key in enumerate(keys, start=1):
        print('{}. {}'.format(i, key))
    # decrement by one for index lookup
    key_input = int(input('\nSelect a key: '))-1

    modes = data['scales'][scale_input]['modes']
    mode_input = 0
    # not every scale has modes
    if len(modes) > 0:
        print('\nThe following modes are available:\n')
        for i, mode in enumerate(modes, start=1):
            print('{}. {}'.format(i, mode))
        # decrement by one for index lookup
        mode_input = int(input('\nSelect a mode: '))-1

    # FIXME hardcoding sharp list until we give the user a choice
    notes = create_sharp_notes_list()
    intervals = data['scales'][scale_input]['intervals']
    sl = len(notes)
    il = len(intervals)
    scale = []
    for i in range(mode_input, mode_input + il):
        scale.append(notes[key_input % sl])
        key_input += intervals[i % il]
    return scale

def generate_riff(notes: 'list', phrase: 'str') -> ('list', 'list'):
    """Maps the characters of a phrase to a list of notes"""

    if len(phrase) == 0:
        return

    phrase = phrase.upper()
    offset = ord('A')
    sl = len(notes)

    scale_degrees = []
    riff = []
    for c in list(phrase):
        scale_degree = (ord(c) - offset) % sl
        scale_degrees.append(scale_degree)
        riff.append(notes[scale_degree])

    return (riff, scale_degrees)

def main_loop():
    notes = build_scale()
    phrase = input("\nEnter a phrase to riffify: ")
    riff, scale_degrees = generate_riff(notes, phrase)
    print('\n' + ' - '.join(riff))
    # scale degrees come back as integers and are zero-indexed for programmatic
    # use, so we need to plus-one and convert them for display
    print(' - '.join(map(str, map(lambda x: x + 1, scale_degrees))))

signal.signal(signal.SIGINT, exit_handler)

print("\nStarting RiffMaker, CTRL-C to exit...")
load_data()
while True:
    main_loop()