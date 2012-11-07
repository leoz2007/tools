from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.conf import settings
import os

### Delete database
if os.path.isfile(settings.DB_PATH):
    os.remove(settings.DB_PATH)

## Sync the db
call_command('syncdb', interactive=False)

## Run application
application = WSGIHandler()
