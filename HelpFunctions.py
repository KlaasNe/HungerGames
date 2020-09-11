SPECIAL_CHARS = ["*", "_", "~"]


def get_int(input_msg):
    try:
        value = int(input(input_msg))
        return value if value > -1 else get_int(input_msg)
    except ValueError:
        print("This is not a whole number.")
        return get_int(input_msg)


def enter():
    try:
        input("Press <Enter> to continue...")
    except Exception:
        pass


def add_escapes(text):
    escaped_txt = ""
    for char in range(len(text)):
        if text[char] in SPECIAL_CHARS:
            escaped_txt += "\\"
        escaped_txt += text[char]
    return escaped_txt
