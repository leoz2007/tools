# Django settings for jibli_v1 project.

import os
import django

DEPLOY_MODE = False
DEV_MODE = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if DEPLOY_MODE:
    LOG_ROOT = os.path.join(PROJECT_ROOT, '../log')
else:
    LOG_ROOT = os.path.join(PROJECT_ROOT, '/tmp/')
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
WEBSITE_ROOT = os.path.join(PROJECT_ROOT,'website')
GEOIP_PATH = os.path.join(PROJECT_ROOT,'GeoIP')
DOMAIN_PATH, PROJECT_NAME = os.path.split(PROJECT_ROOT)
PROJECT_DOMAIN = os.path.split(DOMAIN_PATH)[1] if DEPLOY_MODE else 'jibli'

FACEBOOK_APP_ID                   = '390281834345585'
FACEBOOK_API_SECRET               = '342b5cfd357eaac1f8c0542643f83cb9'

#
# CONFIG BY ThinkIT
#

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
DB_PATH = os.path.join(PROJECT_ROOT,'db')

DATABASES = {
    'default': {
        'ENGINE' : 'django_mongodb_engine',
        'NAME' : PROJECT_DOMAIN,
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# User profile to use with django auth
AUTH_PROFILE_MODULE = 'website.JibliUser'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'
SITE_ID=u'4fc484656e95521500000000'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT,'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/s/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/s/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT,'site_media'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_5hxunbi2x$q05b-1-y&%t$y^swc9s7yh^k!@(5p&c17ax$ev)'

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.request",
"django.contrib.messages.context_processors.messages")

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
## Add user_id cookie if user is authenticated (needed for websockets)
    'website.middleware.cookies.CookiePostHandlerMiddleware',
 )

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATE_DIRS = (
    os.path.join(WEBSITE_ROOT,'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [ 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django.contrib.sites',
    'website',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.humanize',
    'django_mongodb_engine',
 ]

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry', 'debug_file'],
        },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        'simple': {
            'format': '[%(levelname)s] -%(module)s- "%(message)s"'
            },
        },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            },
        'mail_admins': {
            'level': 'CRITICAL',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'debug.log'),
            'maxBytes': '16777216', #16 megabytes
            'formatter': 'verbose'
            },
       'access_file': {
            'level': 'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'access.log'),
            'maxBytes': '16777216', #16 megabytes
            'formatter': 'simple'
            },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['debug_file', 'sentry'],
            'propagate': False,
        },
       'raven': {
            'level': 'DEBUG',
            'handlers': ['debug_file'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['debug_file'],
            'propagate': False,
        }, 
    },
}

try:
    from social_settings import *
except:
    pass

#
# The following is use by website.fb_models
# to easilly post object to FB
#

# The following field specify the protocol facebook must use to scrap our website
FACEBOOK_PROTOCOL='http'

# Our app namespace as definer in Facebook Developers website
FACEBOOK_NAMESPACE='jibliapp'

# If specified the following field will overwrite
# the natural behavior of fb_model that will take the domain from Django Site
# This will allow you to test using sampes.ogp.me
#FACEBOOK_DNAME='samples.ogp.me'


## CELERY WORKER CONFIG
if DEPLOY_MODE:
    BROKER_URL = 'mongodb://localhost:27017/celery-%s' % PROJECT_DOMAIN
    INSTALLED_APPS += ('djcelery',)
    import djcelery
    djcelery.setup_loader()

# Used to determine how many more results are shown on the client using the pagination
LIMIT_PAGINATION = 30

# Used to determine how many announces we see (at load) in newsfeed on home page
LIMIT_NEWSFEED_INIT = 5

## ZMQ CONTEXT MUST BE UNIQUE AND CLEANLY SHUT DOWN

if not DEPLOY_MODE:
    import zmq
    import atexit

    def clean_context(context):
        context.term()

    context = zmq.Context()
    ZMQ_CONTEXT = context
    atexit.register(clean_context, context)

# Amazon s3 settings (used for data uploads)
import boto
DEV_UPLOAD_DOMAIN = 'https://jibli.s3.amazonaws.com'
DEV_UPLOAD_ORIG_IMG_FOLDER = '/images/dev/original/'                  # folder for original announces photos 
DEV_UPLOAD_THUMB_IMG_FOLDER = '/images/dev/thumbnails/'               # folder for announces thumbnails
DEV_UPLOAD_LARGE_THUMB_IMG_FOLDER = '/images/dev/large_thumbnails/'   # folder for announces large thumbnails

PROD_UPLOAD_DOMAIN = 'https://jibli.s3.amazonaws.com'
PROD_UPLOAD_ORIG_IMG_FOLDER = '/images/prod/original/'                # folder for original announces photos 
PROD_UPLOAD_THUMB_IMG_FOLDER = '/images/prod/thumbnails/'             # folder for announces thumbnails
PROD_UPLOAD_LARGE_THUMB_IMG_FOLDER = '/images/dev/large_thumbnails/'  # folder for announces large thumbnails

S3_ACCESS_KEY_ID = 'AKIAIUQL6PPVWGNTATYQ'
S3_SECRET = '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'
S3_HANDLE = boto.connect_s3(S3_ACCESS_KEY_ID, S3_SECRET)



### Seentry configuration
SENTRY_DSN= 'http://552e18b8598641eeacb6e2dac9c05b86:21e56e7d4fd34312ba7bf83ee6f391a1@sentry.tkit.me/1'
