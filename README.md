# GeoDE
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

Function calls in api.py depends on installation of python3.9 or above version

Some issues may occur with psycopg2 on new Apple Silicon Macs. Try installing necessary packages manually (instead of through the requirements document)


## Future directions

We are very hopeful that GeoDE can provide value to members of the Carleton community well into the future!
In building our product, there were several features we did not implement, either due to constraints of time or scope. We hope that they can be fully realized in future iterations of this project. Please visit the Issues tab to learn more about future directions of GeoDE.
