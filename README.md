# sisense
[![Documentation Status](https://readthedocs.org/projects/sisense/badge/?version=latest)](https://sisense.readthedocs.io/en/latest/?badge=latest)

Python interface for Sisense API.

### Note
In development.

## Install
Not available **yet**.
```
pip install sisense
```

## Getting started
```{python}
from sisense import Sisense

sisense = Sisense(host, token)
datamodel = sisense.datamodel

new_datamodel = datamodel.clone('Datamodel copy')

build = new_datamodel.start_build('replace_all')
build.stop()  # or new_datamodel.stop_builds() to stop all builds 

```

## Testing
```
make api-test
```
