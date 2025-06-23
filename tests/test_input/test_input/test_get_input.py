"""Test for the intended functionallity of input.get_input"""
import pytest
from typing import Literal, Any
from src.save_input.input import get_input


# ============================================================================================================================ #
#                                                       Test IO                                                                #
# ============================================================================================================================ #
def test_empty_answer_exists(monkeypatch) -> None:
    monkeypatch.setattr("builtins.input", lambda x: "")
    assert get_input("Prompt", max_question=1) is None


@pytest.mark.parametrize('__input', ["halli!", "halløj!", "En mand i dame tøj", "..."])
def test_non_empty_input(monkeypatch, __input: str) -> None:
    monkeypatch.setattr("builtins.input", lambda x: __input)
    assert get_input("Prompt", max_question=1) == __input


@pytest.mark.parametrize("myprompt", ["Hard", "Rock", "Hallelujah"])
def test_prompt(monkeypatch, myprompt: str) -> None:
    """Check if the message is prompted to the user correctly!

    builtins.print is monkeypatches to save prompted message to valiable 'output'
    and return an empty string to exist 'get_input' messsage.
    """
    # Setup monkeypatch
    output: list[str] = []
    def mockinput(prompt: str) -> Literal[""]:
        output.append(prompt)
        return ""
    monkeypatch.setattr("builtins.input", mockinput)

    # Run command which should output to user
    assert get_input(myprompt) is None

    # Compare strings
    assert [myprompt, ] == output


# ============================================================================================================================ #
#                                                       Interpretation                                                         #
# ============================================================================================================================ #
def example_interpretor(string: str) -> tuple[None | Any, str]:
    match string:
        case 'yes':
            return True, ""
        case 'no':
            return False, ""

    try:
        return int(string), ""
    except ValueError:
        pass

    try:
        return float(string), ""
    except ValueError:
        pass

    try:
        return complex(string), ""
    except ValueError:
        pass

    return None, f"Cannot interpret input {string}"


@pytest.mark.parametrize(
    '__input,expected',
    [
        ('yes', True),
        ('no', False),

        ('1231', 1231),
        ('3333333', 3333333),

        ('12.0', 12.0),
        ('3.1415', 3.1415),

        ('j', 1j),
        ('1+j', 1 + 1j),
        ('inf', float('inf'))
    ])
def test_if_interpretation_correctly(monkeypatch, __input: str, expected: Any) -> None:
    monkeypatch.setattr('builtins.input', lambda x: __input)
    assert expected == get_input("", interpretor=example_interpretor)


def test_if_interpretation_fails(monkeypatch) -> None:
    """Test that the question is asked again if users

    If an interpretation fails should be signalled to the user.
    """
    # Create mock input function
    nonsense_strings = ["dajk", "sdaædaspåsd", "dddddddd", "AAAAA", "Bla", "yes"]
    current_index = 0
    def mockinput(_: str) -> str:
        nonlocal current_index, nonsense_strings
        string = nonsense_strings[current_index]
        current_index += 1
        return string
    monkeypatch.setattr('builtins.input', mockinput)

    # Create mock print function
    output: list[str] = []
    def mockprint(*strings) -> None:
        output.append("".join(strings))
    monkeypatch.setattr('builtins.print', mockprint)

    # Run test
    assert True is get_input("", interpretor=example_interpretor)

    # Check if errorstring was provided
    for _in, _out in zip(nonsense_strings, output):
        assert f"Cannot interpret input {_in}" == _out


# ============================================================================================================================ #
#                                                       Validation                                                             #
# ============================================================================================================================ #
def example_validator(x: str) -> tuple[bool, str]:
    if 3 == (length := len(x)):
        return (True, "")
    return False, "String is too " + ("short" if length < 3 else "long")


def test_validation_sucess(monkeypatch) -> None:
    monkeypatch.setattr('builtins.input', lambda x: 'hejsa')
    assert 'hejsa' == get_input("", validator=lambda x: (x.startswith('h'), ""))


def test_validation_fails(monkeypatch) -> None:
    # Create mock input function
    nonsense_strings = ["dajk", "sdaædaspåsd", "dddddddd", "AAAAA", "Bla"]
    current_index = 0
    def mockinput(_: str) -> str:
        nonlocal current_index, nonsense_strings
        string = nonsense_strings[current_index]
        current_index += 1
        return string
    monkeypatch.setattr('builtins.input', mockinput)

    # Create mock print function
    output: list[str] = []
    def mockprint(*strings) -> None:
        output.append("".join(strings))
    monkeypatch.setattr('builtins.print', mockprint)

    # Run test
    assert 'Bla' == get_input("", validator=example_validator)

    # Check if errorstring was provided
    for _in, _out in zip(nonsense_strings, output):
        match _out:
            case "String is too short":
                pass
            case "String is too long":
                pass
            case _:
                assert False, f"Got output: {_out}"


# ============================================================================================================================ #
#                                                       Limitations                                                            #
# ---------------------------------------------------------------------------------------------------------------------------- #
# Has been moved to tests/test_input/test_limits.py                                                                            #
# ============================================================================================================================ #
