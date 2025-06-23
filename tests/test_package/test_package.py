

def test_pytest_can_run() -> None:
    assert True


def test_import_package() -> None:
    import save_input as _


def test_import_get_input() -> None:
    from save_input.input import get_input as _
