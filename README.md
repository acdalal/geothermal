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



## Possible new features


### Caching database results

Querying the database for a wide time range can take a while. Caching some of the most recent database results or all data for the last year can help speed up large queries.

### Optimize backed code with better data structures
Arrays from the `numpy` library are often faster than Python arrays. Large arrays are used often in the backend to store query information and data for the graphs, so switching from default Python arrays to `numpy` arrays can lead to an improvement in performance.

### Futureproof the queries
Currently we allow the user to enter any possible depth, and use the measurement interval in the database to pick the closest depth that actually has measurements there. However, if the measurement interval was changed in the future, it might cause some of the queries to output false data. Modifying the queries to use a different mechanism for picking depth will make the project more reliable long-term.

Another way to achieve this would be to query each measurement configuration separately. These configurations are stored in the database and contain general information about the DTS unit, including the measurement interval. Sending a separate query for each configuration can resolve this issue as well.

### Simplified custom query

Currently we suport a custom SQL query for more advanced users. This is aimed at users with a better understanding of the geothermal system, but right now it also relies on them knowing SQL. Adding a less coding-oriented custom query would make it more accessible.

### Side-by-side graphs for Temperature Profile

This was a requested feature that we didn't have time to implement. The idea is to let the user fill out up to 3 Temperature Profile forms by clicking on a button to generate another form. Submitting one of the forms would submit all of them and output three graphs on one page.

This would let the user compare the temperature profile for several ranges, something that currently can only be achieved by opening GeoDE on multiple browser tabs or downloading the graph image before submitting another query.
