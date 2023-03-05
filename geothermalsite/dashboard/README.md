# Dashboard Application
The `geothermalsite/dashboard` directory contains the core app, made up of the API and frontend.

## Key Directories
`dashboard/helper` contains the API (api.py), as well as constants (constants.py) and helper functions for
- storing boreholes as a class (boreholes.py)
- creating database queries (createQueries.py)
- processing user forms (processUserForms.py)
- rendering templates for the frontend (renderFunctions.py)
- creating visualizations (visualization.py)
- logging app activity to a log file (logging.py)

`dashboard/static` contains static files, which Django defines as CSS, JavaScript, or img files.

`dashboard/templates` contains all the HTML files that are rendered to the frontend, drawing on the
static files for styling and functionality.

**Note:** `dashboard/migrations` would store information used by Django to take changes from the models
(dashboard/models.py) and modify the database schema accordingly, but since this the database permissions of the
app are *read-only*, dashboard uses neither models nor migrations.

## Key Files
`forms.py` contains classes for all of the [Django forms](https://docs.djangoproject.com/en/4.1/topics/forms/) that the dashboard app uses.

`views.py` contains all of the [Django views](https://docs.djangoproject.com/en/4.1/topics/http/views/) for processing web requests and returning web responses.

`urls.py` maps URL routes to views functions.

`middleware.py` contains custom [Django middleware](https://docs.djangoproject.com/en/4.1/topics/http/middleware/) that does extra processing 
when HTTP requests/responses are executed. This is how the app logs user IP addresses when the user submits a query.

**Note:** other files, such as admin.py & test.py, are Django boilerplate but are not used by this application.

## Overview of App Functionality
Learning how Django functions as a full-stack framework was a major challenge in our project. The [Django documentation](https://docs.djangoproject.com/en/4.1/) 
is extremely helpful and provides lots of examples, but in an effort to summarize how our dashboard app works, 
here's an overview of the flow between files and directories:

1. When a user points their browser to a URL that matches one of the paths specified in `urls.py`, the corresponding function in `views.py` is executed,
taking an HttpRequest object as input.
2. If the HttpRequest method is **GET**, the views function renders the specified template in the `dashboard/templates` directory with any ready-to-be-filled-out forms that may be included in it.
If the method is **POST**, the user has submitted a form. In this case, the views function renders the specified template, as well as the data that
is returned from the database for the parameters contained in the form that the user submitted.
3. If you look deeper into `views.py`, you will see that a given function, such as *index*, calls many of the helper functions from `dashboard/helpers`. 
First, it retrieves data from the submitted form using `helper/processUserForms.py`. Then, it uses the **API** `helper/api.py` to query the 
database with the filters given in the form. Finally, it uses `helper/renderFunctions.py` to render the appropriate template to the frontend, 
where the user will see the data they asked for.
