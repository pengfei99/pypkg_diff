import pathlib

import pytest

from src.pypkg_diff.pname_parser import (get_pkg_names_from_req, get_pkg_names_from_pypi_file, get_missing_pkgs, compare_req_pypi,
                                         get_pkg_names_from_pypi_db)

@pytest.fixture()
def test_data_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.resolve() / "data"

@pytest.fixture()
def sample_req_path(test_data_dir: pathlib.Path) -> pathlib.Path:
    return test_data_dir / "u-requirements.txt"

@pytest.fixture()
def sample_pypis_path(test_data_dir: pathlib.Path) -> pathlib.Path:
    return test_data_dir / "casd-packages.csv"

@pytest.fixture()
def sample_pypis_db_path(test_data_dir: pathlib.Path) -> pathlib.Path:
    return test_data_dir / "packages.sqlite"

def test_get_pkg_names_from_req(sample_req_path: pathlib.Path) -> None:
    pkg_list = get_pkg_names_from_req(sample_req_path)
    print(pkg_list)


def test_get_pkg_names_from_pypi(sample_pypis_path: pathlib.Path) -> None:
    pkg_list = get_pkg_names_from_pypi_file(sample_pypis_path)
    print(pkg_list)

def test_get_missing_pkgs(sample_req_path: pathlib.Path, sample_pypis_path) -> None:
    req_pkgs = get_pkg_names_from_req(sample_req_path)
    pypi_pkgs = get_pkg_names_from_pypi_file(sample_pypis_path)
    missing_pkgs = get_missing_pkgs(req_pkgs, pypi_pkgs)
    print(missing_pkgs)

def test_compare_req_pypi_with_casd_file(sample_req_path: pathlib.Path, sample_pypis_path) -> None:
    req_pkgs = get_pkg_names_from_req(sample_req_path)
    pypi_pkgs = get_pkg_names_from_pypi_file(sample_pypis_path)
    compare_req_pypi(req_pkgs, pypi_pkgs)

def test_get_pkg_names_from_pypi_db(sample_pypis_db_path: pathlib.Path) -> None:
    pypi_pkgs = get_pkg_names_from_pypi_db(sample_pypis_db_path)
    pypi_pkgs_nb = len(pypi_pkgs)
    print(f"total packages number: {pypi_pkgs_nb}")

def test_compare_req_pypi_with_db(sample_req_path: pathlib.Path, sample_pypis_db_path) -> None:
    req_pkgs = get_pkg_names_from_req(sample_req_path)
    pypi_pkgs = get_pkg_names_from_pypi_db(sample_pypis_db_path)
    compare_req_pypi(req_pkgs, pypi_pkgs)