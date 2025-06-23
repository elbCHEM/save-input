from save_input.input import get_input


VALID_YES_STRINGS = {'y', 'yes', 'ja'}
VALID_NO_STRINGS = {'n', 'no', 'nej'}


def interpretor(string: str) -> None | bool:
    """Homogenize string and check if they match valid answers"""
    string = string.strip().lower()

    if string in VALID_YES_STRINGS:
        return True
    if string in VALID_NO_STRINGS:
        return False
    return None


def get_yes_no(prompt: str, **options) -> None | bool:
    return get_input(prompt, interpretor=interpretor, **options)
