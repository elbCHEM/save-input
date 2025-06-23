from typing import Literal, Callable, Any


type Interpretor[T] = Callable[[str,], T]
type Validator[T] = Callable[[T], tuple[bool, str]]


_MAX_QUESTIONS_ASKED = 1_000


class TooManyQuestionAsked(Exception):
    question_asked: int

    def __init__(self, question_asked: int) -> None:
        self.question_asked = question_asked
        super().__init__(f"Too many question asked - Finished after {question_asked} questions.")


def identity(x: Any) -> Any:
    return x


def validate_nothing(x: Any) -> tuple[Literal[True], Literal[""]]:
    return (True, "")


def get_input(
    prompt: str,
    /,
    interpretor: Interpretor = identity,
    validator: Validator = validate_nothing,
    max_question: int = _MAX_QUESTIONS_ASKED,
) -> None | Any:
    if (max_question := min(max_question, _MAX_QUESTIONS_ASKED)) <= 0:
        raise ValueError(f"'max_questions' must be a positive integer - Was {max_question}")

    for n in range(max_question):
        if "" == (raw_input_string := input(prompt)):
            return None
        if (interpreted_input := interpretor(raw_input_string)) is None:
            continue

        isvalid, errorstring = validator(interpreted_input)
        if isvalid:
            return interpreted_input
        print(errorstring)

    raise TooManyQuestionAsked(n)
