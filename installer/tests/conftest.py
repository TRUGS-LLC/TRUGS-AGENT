"""Prepared public inputs for complete offline command regressions."""

from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--repositories", type=Path, help="prepared public checkouts")


@pytest.fixture
def prepared_repositories(request):
    path = request.config.getoption("--repositories")
    if path is None:
        pytest.skip("complete command regressions need --repositories")
    return path.resolve()
