"""Test if the limits of the get_input function is applied correctly"""
import pytest
from src.save_input.input import get_input, TooManyQuestionAsked, _MAX_QUESTIONS_ASKED


VERY_LARGE_INTEGER = 0xFFFFFFFF


# ============================================================================================================================ #
#                                                       Test limits                                                            #
# ============================================================================================================================ #
def test_max_question_asked(monkeypatch) -> None:
    """Check that failsafe exists if I keep supplying false aswers"""
    monkeypatch.setattr("builtins.input", lambda x: 'dsakdas')
    with pytest.raises(TooManyQuestionAsked):
        get_input("Prompt doesn't matter here", validator=lambda x: (False, ""))


@pytest.mark.parametrize('n', [1, 10, 50])
def test_max_question_userdefined(monkeypatch, n: int) -> None:
    """Check if user can change number of wrong answers accepted"""
    monkeypatch.setattr("builtins.input", lambda x: 'dsajkd')
    with pytest.raises(TooManyQuestionAsked) as error:
        get_input("Prompt doesn't matter here",
                  validator=lambda x: (False, ""),
                  max_question=n
                  )
        assert n == error.question_asked  # type: ignore[attr-defined]


def test_max_question_hard_limit(monkeypatch) -> None:
    """Check if the hard limit on number of questions is enforced"""
    monkeypatch.setattr("builtins.input", lambda x: 'dsajkd')
    with pytest.raises(TooManyQuestionAsked) as error:
        get_input("Prompt doesn't matter here",
                  validator=lambda x: (False, ""),
                  max_question=VERY_LARGE_INTEGER
                  )
        assert _MAX_QUESTIONS_ASKED == error.max_question  # type: ignore[attr-defined]


@pytest.mark.parametrize('n', [-0xFFFFFF, -1, 0, ])
def test_max_question_too_small(monkeypatch, n: int) -> None:
    """Check if limit does not break if too small value if provided for max"""
    monkeypatch.setattr("builtins.input", lambda x: 'dsajkd')
    with pytest.raises(ValueError):
        get_input("Prompt doesn't matter here", validator=lambda x: (False, ""), max_question=n)


@pytest.mark.parametrize('n', [[], "", "fdjksfsdj", {}])
def test_max_question_non_sense(monkeypatch, n) -> None:
    """Check if exception is raised if nonsense value is provided for max questions"""
    monkeypatch.setattr("builtins.input", lambda x: 'dsajkd')
    with pytest.raises(TypeError):
        get_input("Prompt doesn't matter here", validator=lambda x: (False, ""), max_question=n)
