from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command

import os

## Generate static files
if not os.path.exists('static'):
    os.mkdir('static')
call_command('collectstatic', interactive=False)


### Drop database
from django.conf import settings
import pymongo
con = pymongo.Connection()
con.drop_database(settings.PROJECT_DOMAIN)

### Create site identifiers
from django.contrib.sites.models import Site
s, created = Site.objects.get_or_create(domain=settings.PROJECT_DOMAIN + '.tkit.me')

## Set the new siteid in settings
settings.SITE_ID=s.id

## Sync the db
call_command('syncdb', interactive=False)

## Run application
application = WSGIHandler()
