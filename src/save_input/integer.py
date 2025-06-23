from typing import Optional
from save_input.input import get_input
from save_input.bounds_checker import get_bounds_checker


def get_integer(prompt: str,
                /,
                min_included: Optional[int] = None,
                max_included: Optional[int] = None,
                min_excluded: Optional[int] = None,
                max_excluded: Optional[int] = None,
                **options,
                ) -> None | int:
    validator = get_bounds_checker(
        min_included=min_included,
        max_included=max_included,
        min_excluded=min_excluded,
        max_excluded=max_excluded,
    )
    return get_input(prompt,
                     interpretor=integer_interpretor,
                     validator=validator,
                     **options
                     )


def integer_interpretor(string: str) -> None | int:
    try:
        return int(string)
    except ValueError:
        return None
