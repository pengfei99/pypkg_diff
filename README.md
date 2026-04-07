# pypkg_diff

The goal of this tool is to determine if our private pypi server contains the required packages of the 
user `requirements.txt`

## Sample code

For the package names from the `requirements.txt`, it's quite simple, you can use the below function to get the pakcage
name list.

```python
pkg_list = get_pkg_names_from_req(sample_req_path)
```

For the package names in your private pypi server, we provide two solution. If you have a csv file, you can get
the list with the function `get_pkg_names_from_pypi_file`. We suppose the first column of the csv file is the 
package name.

```python
pkg_list = get_pkg_names_from_pypi_file(sample_pypis_path)
```

If you have sqlite database, you can get the list with the function `get_pkg_names_from_pypi_db`.

```python
pypi_pkgs = get_pkg_names_from_pypi_db(sample_pypis_db_path)
```

You can get the diff between user requirements.txt and your pypi server with `compare_req_pypi`. This function
will return the stats and missing package name

```python
compare_req_pypi(req_pkgs, pypi_pkgs)
```