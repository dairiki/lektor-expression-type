# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from lektor.builder import Builder
from lektor.context import Context
from lektor.project import Project


@pytest.fixture(scope="session")
def site_path():
    return Path(__file__).parent / 'test-site'


@pytest.fixture(scope="session")
def lektor_env(site_path):
    return Project.from_path(str(site_path)).make_env(load_plugins=False)


@pytest.fixture
def lektor_pad(lektor_env):
    return lektor_env.new_pad()


@pytest.fixture
def lektor_builder(lektor_pad, tmp_path):
    return Builder(lektor_pad, str(tmp_path))


@pytest.fixture
def lektor_build_state(lektor_builder):
    with lektor_builder.new_build_state() as build_state:
        yield build_state


@pytest.fixture
def lektor_context(lektor_pad):
    with Context(pad=lektor_pad) as ctx:
        yield ctx
