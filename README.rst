Meal Planner
==============================

A meal planner web application written in Django.


LICENSE: BSD

Settings
------------

Meal Planner relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the 'Meal Planner' environment variables to their Django setting:

======================================= =========================== ============================================== ===========================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ===========================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
DJANGO_CACHES                           CACHES                      locmem                                         memcached
DJANGO_DATABASES                        DATABASES                   See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_EMAIL_BACKEND                    EMAIL_BACKEND               django.core.mail.backends.console.EmailBackend django.core.mail.backends.smtp.EmailBackend
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
======================================= =========================== ============================================== ===========================================

* TODO: Add vendor-added settings in another table

Getting up and running
----------------------

1. Run ``vagrant up`` to create, start, and provision your development virtual machine.
2. Run ``vagrant ssh`` to ssh into the newly provisioned virtual machine.
3. Run ``python /vagrant/meal_planner/manage.py createsuperuser`` to create a superuser

You can now run ``grunt serve`` while SSHed into the ``/vagrant`` directory to serve the app, which you can then view from your host at localhost:8000. In addition, the uwsgi server will be reloaded automatically upon file changes.

Note that when any included dependency changes its static files, you must run ``collectstatic -l -i sass`` to update the staticfiles directory, which is where nginx forwards ``/static`` requests to.

Deployment
------------

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups:auto-month
    heroku addons:add sendgrid:starter
    heroku addons:add memcachier:dev
    heroku pg:promote DATABASE_URL
    heroku config:set DJANGO_CONFIGURATION=Production
    heroku config:set DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    heroku config:set SENDGRID_USERNAME=YOUR_SENDGRID_USERNAME_HERE
    heroku config:set SENDGRID_PASSWORD=YOUR_SENDGRID_PASSWORD_HERE
    git push heroku master
    heroku run python meal_planner/manage.py syncdb --noinput --settings=config.settings
    heroku run python meal_planner/manage.py migrate --noinput --settings=config.settings
    heroku run python meal_planner/manage.py createsuperuser
    heroku open
