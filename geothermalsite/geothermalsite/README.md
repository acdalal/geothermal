# Geothermalsite Application
This directory contains the application that handles settings and configurations for the project.

`urls.py` maps URLs to the `../dashboard` application, and has the capability to map URLs to an admin page as well.

`settings.py` contains all of this project's [Django settings](https://docs.djangoproject.com/en/4.1/topics/settings/), including settings for, among other things,
- connecting to the geothermal database
- establishing a static files directory
- configuring an automatic logging system
- executing Django middleware
