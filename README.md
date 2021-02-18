# GW Superevent EM follow-up

This reusable TOM Toolkit app provides support for gravitational wave (GW)
superevent electromagnetic (EM) follow up observations.  

## Installation

1. Install the module into your TOM environment:
    ```bash
    pip install tom_superevents
   ```

2. In your project `settings.py`, add `tom_superevents` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = [
        ...
        'tom_superevents',
    ]
    ```

3. Include the tom_superevent URLconf in your project `urls.py`:
   ```python
   urlpatterns = [
        ...
        path('superevents/', include('tom_superevents.urls')),
   ]
   ```

4. Run ``python manage.py migrate`` to create the tom_superevent models.


## Running the tests

In order to run the tests, run the following in your virtualenv:

`python tom_superevent/tests/run_tests.py`

