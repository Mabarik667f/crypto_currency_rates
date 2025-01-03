import pytest
from pytest import MonkeyPatch


@pytest.fixture
def change_dir_to_tests(monkeypatch: MonkeyPatch):
    monkeypatch.chdir(path="./tests")
