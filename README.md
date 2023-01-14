# geothermal
Repository for the Carleton Geothermal Data API Comps project


## To begin working
Run these commands:\
`pip install -r requirements.txt` \
`pre-commit install` \
`pip install pre-commit-hooks`

## Troubleshooting
One of the packages relies on a specific version of the Python regex library, so if pip fails, try running \
`ARCHFLAGS="-arch x86_64" pip install -r requirements.txt`.

If psycopg2 doesn't install on Mac, try running \
`brew install openssl` \
`export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/`

Function calls in api.py depends on installation of python3.9 or above version \

Some issues may occur with psycopg2 on new Apple Silicon Macs. Try installing necessary packages manually (instead of through the requirements document) \

## Project structure and key files
`geothermalsite/settings.py` contains project settings such as installed apps and database configurations

`geothermalsite/urls.py` specifies routing and what applications handle what URLs

`dashboard/views.py` handles user forms and POST requests

`dashboard/api.py` queries the database and returns cleaned data to `views.py`
