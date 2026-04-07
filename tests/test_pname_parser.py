import pathlib

import pytest

from src.pypkg_diff.pname_parser import get_pkg_names_from_req, get_pkg_names_from_pypi, get_missing_pkgs, compare_req_pypi

@pytest.fixture()
def test_data_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.resolve() / "data"

@pytest.fixture()
def sample_req_path(test_data_dir: pathlib.Path) -> pathlib.Path:
    return test_data_dir / "u-requirements.txt"

@pytest.fixture()
def sample_pypis_path(test_data_dir: pathlib.Path) -> pathlib.Path:
    return test_data_dir / "casd-packages.csv"

def test_get_pkg_names_from_req(sample_req_path: pathlib.Path) -> None:
    pkg_list = get_pkg_names_from_req(sample_req_path)
    print(pkg_list)


def test_get_pkg_names_from_pypi(sample_pypis_path: pathlib.Path) -> None:
    pkg_list = get_pkg_names_from_pypi(sample_pypis_path)
    print(pkg_list)

def test_get_missing_pkgs(sample_req_path: pathlib.Path, sample_pypis_path) -> None:
    req_pkgs = get_pkg_names_from_req(sample_req_path)
    pypi_pkgs = get_pkg_names_from_pypi(sample_pypis_path)
    missing_pkgs = get_missing_pkgs(req_pkgs, pypi_pkgs)
    print(missing_pkgs)

def test_compare_req_pypi(sample_req_path: pathlib.Path, sample_pypis_path) -> None:
    req_pkgs = get_pkg_names_from_req(sample_req_path)
    pypi_pkgs = get_pkg_names_from_pypi(sample_pypis_path)
    compare_req_pypi(req_pkgs, pypi_pkgs)