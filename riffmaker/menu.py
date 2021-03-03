import os, signal, sys
import library

config = {}


def exit_handler(signum, frame):
    if signum == signal.SIGINT:
        print("\nInterrupt received, shutting down")
    else:
        print("\nRock out!")
    sys.exit(0)


def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def create_riff():
    notes = library.build_scale(config["scale"], config["key"], config["mode"])
    phrase = input("\nEnter a phrase to riffify: ")
    riff, scale_degrees = library.generate_riff(notes, phrase)
    print("\n" + " - ".join(riff))
    # scale degrees come back as integers and are zero-indexed for programmatic
    # use, so we need to plus-one and convert them for display
    print(" - ".join(map(str, map(lambda x: x + 1, scale_degrees))))
    _ = input("\nPress enter to continue...")


def print_header():
    clear_screen()
    print("RIFFMAKER")
    print("=========")


def print_configuration():
    print(
        "Scale: {} | Key: {} | Mode: {}\n".format(
            library.get_scales()[config["scale"]],
            library.create_full_notes_list()[config["key"]],
            library.get_modes(config["scale"])[config["mode"]],
        )
    )


def configure_scale():
    scales = library.get_scales()
    print_header()
    print("\nThe following scales are available:\n")
    for i, scale in enumerate(scales, start=1):
        print("{}. {}".format(i, scale))
    # decrement by one for index lookup
    scale_input = -1
    try:
        scale_input = int(input("\nSelect a scale: ")) - 1
    except ValueError:
        pass
    if scale_input < 0 or scale_input >= len(scales):
        configure_scale()
    else:
        config["scale"] = scale_input


def configure_key():
    keys = library.create_full_notes_list()
    print_header()
    print("\nThe following keys are available:\n")
    for i, key in enumerate(keys, start=1):
        print("{}. {}".format(i, key))
    # decrement by one for index lookup
    key_input = -1
    try:
        key_input = int(input("\nSelect a key: ")) - 1
    except ValueError:
        pass
    if key_input < 0 or key_input >= len(keys):
        configure_key()
    else:
        config["key"] = key_input


def configure_mode():
    modes = library.get_modes(config["scale"])
    if len(modes) == 0:
        # not every scale has modes
        return
    print_header()
    print("\nThe following modes are available:\n")
    for i, mode in enumerate(modes, start=1):
        print("{}. {}".format(i, mode))
    # decrement by one for index lookup
    mode_input = -1
    try:
        mode_input = int(input("\nSelect a mode: ")) - 1
    except ValueError:
        pass
    if mode_input < 0 or mode_input >= len(modes):
        configure_mode()
    else:
        config["mode"] = mode_input


def print_configure_menu():
    print_header()
    print("1. Change scale")
    print("2. Change mode")
    print("3. Change key")
    print("4. Return to main menu")
    choice = input("\n >> ")
    if choice == "1":
        configure_scale()
    elif choice == "2":
        configure_mode()
    elif choice == "3":
        configure_key()
    elif choice == "4":
        print_main_menu()
    else:
        print_configure_menu()


def configure_all():
    print_header()
    configure_scale()
    configure_key()
    configure_mode()


def print_configure_all_menu():
    print_header()
    print("1. Select scale, mode, and key")
    print("2. Quit")
    choice = input("\n >> ")
    if choice == "1":
        configure_all()
    elif choice == "2":
        exit_handler(None, None)
    else:
        print_configure_all_menu()


def print_main_menu():
    print_header()
    print_configuration()
    print("1. Create riffs")
    print("2. Change scale, mode, or key")
    print("3. Quit")
    choice = input("\n >> ")
    if choice == "1":
        create_riff()
    elif choice == "2":
        print_configure_menu()
    elif choice == "3":
        exit_handler(None, None)
    print_main_menu()


def init():
    print_configure_all_menu()
    print_main_menu()


signal.signal(signal.SIGINT, exit_handler)

print("\nStarting RiffMaker, CTRL-C to exit...")

library.load_data()
init()