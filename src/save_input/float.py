from typing import Optional
from save_input.input import get_input
from save_input.bounds_checker import get_bounds_checker


def get_float(
    prompt: str,
    /,
    min_included: Optional[int | float] = None,
    max_included: Optional[int | float] = None,
    min_excluded: Optional[int | float] = None,
    max_excluded: Optional[int | float] = None,
    **options,
) -> None | int:
    validator = get_bounds_checker(
        min_included=min_included,
        max_included=max_included,
        min_excluded=min_excluded,
        max_excluded=max_excluded,
    )
    return get_input(prompt,
                     interpretor=interpretor,
                     validator=validator,
                     **options
                     )


def interpretor(string: str) -> None | float:
    try:
        return float(string)
    except ValueError:
        return None
