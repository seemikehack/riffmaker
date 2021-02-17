import signal, sys
import library


def exit_handler(signal, frame):
    print("\n\nInterrupt received, shutting down")
    sys.exit(0)


def build_scale() -> "list":
    """Create a list of available notes from which to build a riff."""

    scales = library.get_scales()
    print("\nThe following scales are available:\n")
    for i, scale in enumerate(scales, start=1):
        print("{}. {}".format(i, scale))
    # decrement by one for index lookup
    scale_input = int(input("\nSelect a scale: ")) - 1

    # TODO allow users to switch between sharps and flats
    keys = library.create_full_notes_list()
    print("\nThe following keys are available:\n")
    for i, key in enumerate(keys, start=1):
        print("{}. {}".format(i, key))
    # decrement by one for index lookup
    key_input = int(input("\nSelect a key: ")) - 1

    modes = library.get_modes(scale_input)
    mode_input = -1
    # not every scale has modes
    if len(modes) > -1:
        print("\nThe following modes are available:\n")
        for i, mode in enumerate(modes, start=1):
            print("{}. {}".format(i, mode))
        # decrement by one for index lookup
        mode_input = int(input("\nSelect a mode: ")) - 1

    # FIXME hardcoding sharp list until we give the user a choice
    notes = library.create_sharp_notes_list()
    intervals = library.get_intervals(scale_input)
    sl = len(notes)
    il = len(intervals)
    scale = []
    for i in range(mode_input, mode_input + il):
        scale.append(notes[key_input % sl])
        key_input += intervals[i % il]
    return scale


def main_loop():
    notes = build_scale()
    phrase = input("\nEnter a phrase to riffify: ")
    riff, scale_degrees = library.generate_riff(notes, phrase)
    print("\n" + " - ".join(riff))
    # scale degrees come back as integers and are zero-indexed for programmatic
    # use, so we need to plus-one and convert them for display
    print(" - ".join(map(str, map(lambda x: x + 1, scale_degrees))))


signal.signal(signal.SIGINT, exit_handler)

print("\nStarting RiffMaker, CTRL-C to exit...")

library.load_data()
while True:
    main_loop()