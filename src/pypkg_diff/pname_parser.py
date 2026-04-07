from pathlib import Path
import sqlite3

import pandas as pd
import re

def get_pkg_names_from_pypi_file(file_path:Path) -> list[str]:
    """
    This function read a csv file which describes pypi package names in casd pypi server
    The first column is the package name
    :param file_path:
    :return:
    """
    # 1. Pre-emptive check (Optional but good for specific logging)
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        return []

    # Strategy: Try UTF-8 first (standard), fallback to Latin-1 (Excel/Windows)
    encodings = ["utf-8", "latin-1", "cp1252"]
    for encoding in encodings:
        try:
            # 2. Optimized Read
            # usecols=[0] tells pandas to only load the first column into memory
            df = pd.read_csv(file_path, usecols=[0], encoding=encoding)

            # 3. Handle empty files
            if df.empty:
                return []

            return df.iloc[:, 0].tolist()

        except pd.errors.EmptyDataError:
            print(f"Warning: '{file_path}' is empty.")
        except pd.errors.ParserError:
            print(f"Error: '{file_path}' is not a valid CSV.")
        except Exception as e:
            print(f"The current encoding does not match file encoding, try next encoding: {e}")

    print(f"Error: Could not decode {file_path} with supported encodings.")
    return []

def get_pkg_names_from_pypi_db(db_path:Path) -> list[str]:
    """
    This function read a sqlite file, it will read the table 'packages' and column 'name', return all rows as a list
    :param db_path: The sqlite file path
    :return:
    """
    path = Path(db_path)
    if not path.is_file():
        print(f"Error: Database file '{db_path}' not found.")
        return []

    # Using 'with' as a context manager ensures the connection closes automatically
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Best Practice: Explicitly select only the column you need
            cursor.execute("SELECT name FROM packages")

            # cursor.fetchall() returns a list of tuples: [('affine',), ('pandas',)]
            # We use a list comprehension to "flatten" it into a list of strings
            return [row[0] for row in cursor.fetchall()]

    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def get_pkg_names_from_req(file_path: Path) -> list[str]:
    """
    Reads a requirements.txt file and returns a list of package names.
    """
    package_names = []

    try:
        with open(file_path.as_posix(), "r", encoding="utf-8") as f:
            for line in f:
                # 1. Clean whitespace and ignore empty lines/comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # 2. Handle comments on the same line as code (e.g., flask==2.0 # core dep)
                line = line.split("#")[0].strip()

                # 3. Use Regex to find the first non-alphanumeric character
                # that isn't part of a package name (-, _, .)
                # This catches ==, >=, <=, ~=, >, <, and [extras]
                match = re.match(r"^([a-zA-Z0-9._-]+)", line)
                if match:
                    package_names.append(match.group(1))

        return package_names

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []


def get_missing_pkgs(upkgs: list[str], pypi_pkgs:list[str]) -> list[str]:
    """
    This function checks if upkgs is a subset of pypi_pkgs. If upkgs is a subset of pypi_pkgs, return an empty list
    if not, returns a list of items in upkgs that are missing from pypi_pkgs.
    :param upkgs: user requirements.txt file
    :param pypi_pkgs: casd pypi package names
    :return:
    """
    # Using sets for O(1) membership lookups
    set2 = set(pypi_pkgs)

    # List comprehension to find items in l1 not in set2
    diff = [item for item in upkgs if item not in set2]

    return diff

def compare_req_pypi(req_pkgs: list[str], pypi_pkgs: list[str]) -> None:
    req_pkgs_nb=len(req_pkgs)
    pypi_pkgs_nb = len(pypi_pkgs)
    print(f"The package number in user's requirements.txt is : {req_pkgs_nb}")
    print(f"The package number in casd's pypi server is : {pypi_pkgs_nb}")

    diff_pkgs = get_missing_pkgs(req_pkgs, pypi_pkgs)
    diff_pkgs_nb = len(diff_pkgs)
    print(f"The missing package numbers is : {diff_pkgs_nb}")
    print(f"The missing packages in casd pypi server is : {diff_pkgs}")




