
import pytest
from collections.abc import Iterator

#@pytest.fixture
@pytest.mark.xfail("New test")
def new_test() -> Iterator[None]:
    """Force a test to fail during development"""
    yield
    pytest.fail("New test under development", pytrace=False)
