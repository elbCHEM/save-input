from typing import Optional, Callable


type BoundsChecker = Callable[[int | float], tuple[bool, str]]


def get_bounds_checker(
    *,
    min_included: Optional[int | float] = None,
    max_included: Optional[int | float] = None,
    min_excluded: Optional[int | float] = None,
    max_excluded: Optional[int | float] = None,
) -> BoundsChecker:
    __lower_bounds_checker = lower_bounds_checker(min_included=min_included, min_excluded=min_excluded)
    __upper_bounds_checker = upper_bounds_checker(max_included=max_included, max_excluded=max_excluded)

    def checker(x: int | float) -> tuple[bool, str]:
        is_large_enough, errorstring = __lower_bounds_checker(x)
        if not is_large_enough:
            return (False, errorstring)

        is_large_enough, errorstr = __upper_bounds_checker(x)
        if not is_large_enough:
            return (False, errorstring)

        return (True, "")

    return checker


def upper_bounds_checker(
    *,
    max_included: Optional[int | float] = None,
    max_excluded: Optional[int | float] = None,
) -> BoundsChecker:
    if max_excluded is not None and max_included is not None:
        raise ValueError('Cannot handle both keywords being true')

    # At least one is None
    if max_excluded is not None:
        return upper_bounds_checker_excluded(max_excluded)
    if max_excluded is not None:
        return upper_bounds_checker_included(max_included)

    # Both were None
    return lambda x: (True, "")


def lower_bounds_checker(
    *,
    min_included: Optional[int | float] = None,
    min_excluded: Optional[int | float] = None,
) -> BoundsChecker:
    if min_excluded is not None and min_included is not None:
        raise ValueError('Cannot handle both keywords being true')

    # At least one is None
    if min_excluded is not None:
        return lower_bounds_checker_excluded(min_excluded)
    if min_excluded is not None:
        return lower_bounds_checker_included(min_included)

    # Both were None
    return lambda x: (True, "")


def upper_bounds_checker_included(limit: int | float) -> BoundsChecker:
    def checker(x: int | float) -> tuple[bool, str]:
        return (True, "") if x <= limit else (False, f"Provided answer must be smaller than or equal too {limit:0.2f}")
    return checker


def upper_bounds_checker_excluded(limit: int | float) -> BoundsChecker:
    def checker(x: int | float) -> tuple[bool, str]:
        return (True, "") if x < limit else (False, f"Provided answer must be smaller than {limit:0.2f}")
    return checker


def lower_bounds_checker_excluded(limit: int | float) -> BoundsChecker:
    def checker(x: int | float) -> tuple[bool, str]:
        return (True, "") if x > limit else (False, f"Provided answer must be greater than {limit:0.2f}")
    return checker


def lower_bounds_checker_included(limit: int | float) -> BoundsChecker:
    def checker(x: int | float) -> tuple[bool, str]:
        return (True, "") if x >= limit else (False, f"Provided answer must be greater than or equal to {limit:0.2f}")
    return checker
