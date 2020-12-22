# Sisense API
[![Documentation Status](https://readthedocs.org/projects/sisense/badge/?version=latest)](https://sisense.readthedocs.io/en/latest/?badge=latest)

Python interface for Sisense API.

### Note
In development. Beta version available in:
```shell script
$ pip install -i https://test.pypi.org/simple/ sisense
```

## Install
```shell script
$ pip install sisense
```

## Getting started
```python
from sisense import Sisense

sisense = Sisense(host, token)
datamodel = sisense.datamodel

new_datamodel = datamodel.clone('Datamodel copy')

build = new_datamodel.start_build('replace_all')
build.stop() 

```

## For developers
### Testing
To run all test:
```shell script
$ make api-test
```

#### Support files
In order to test the API functions, you need to supply the following support files:

- `tests/support_files/dashboard.dash`: file created when exporting a dashboard on Sisense
- `tests/support_files/datasecurity.json`: a list of data security rules
- `tests/support_files/hierarchy.json`: a list of hierarchy objects
- `tests/support_files/permission.json`: a list of permission objects
- `tests/support_files/config/api_v09.json`: a JSON with
```json
{
    "host": "<host address>",
    "token": "<API token>",
    "elasticube": "<Elasticube's name used for testing>",
    "user_email": "<User e-mail used for testing>"
}
```
- `tests/support_files/config/api_v1.json`: a JSON with
```json
{
    "host": "<host address>",
    "token": "<API token>",
    "elasticube": "<Elasticube's name used for testing>",
    "user_email": "<User's e-mail used for testing>",
    "group_name": "<Group's name used for testing>",
    "dashboard": "<Dashboard's name used for testing>",
    "folder": "<Folder's name used for testing>"
}
```
- `tests/support_files/config/api_v2.json`: a JSON with
```json
{
    "host": "<host address>",
    "token": "<API token>",
    "datamodel": "<Elasticube's name used for testing>",
    "datamodel.oid": "<Elasticube's ID used for testing (must be the same datamodel)>",
}
```
