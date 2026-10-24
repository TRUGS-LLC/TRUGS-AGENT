"""Prepared public inputs for complete offline command regressions."""

import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--repositories", type=Path, help="prepared public checkouts")
    parser.addoption(
        "--wheelhouse",
        type=Path,
        default=Path(sys.prefix).parent / "wheelhouse",
        help="prepared offline wheels",
    )


@pytest.fixture
def prepared_repositories(request):
    path = request.config.getoption("--repositories")
    if path is None:
        pytest.skip("complete command regressions need --repositories")
    return path.resolve()


@pytest.fixture
def prepared_wheelhouse(request):
    return request.config.getoption("--wheelhouse").resolve()
