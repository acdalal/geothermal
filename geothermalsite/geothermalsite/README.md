# Geothermalsite Application
```
geothermalsite
├── asgi.py
├── config.py
├── __init__.py
├── settings.py
├── urls.py
└── wsgi.py
```


`urls.py` maps URLs to the `dashboard` application, and has the capability to map URLs to an admin page as well.

`settings.py` contains all of this project's [Django settings](https://docs.djangoproject.com/en/4.1/topics/settings/), including settings for, among other things,
- connecting to the geothermal database
- establishing a static files directory
- configuring an automatic logging system

`asgi.py` and `wsgi.py` aren't used since they're supposed to contain settings for framework not implemented in the project. `config.py` has the database credentials; it's not available on this repositry and needs to be requested from the database manager. `__init__.py` is an empty file, and its only purpose is to allow importing from this directory.
