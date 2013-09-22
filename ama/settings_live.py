import os 
from ama.settings import *
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ['CACHE_URL'],
    }
}

INSTALLED_APPS += ('storages',)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

DEFAULT_FILE_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'
STATICFILES_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_static'
EMAIL_BACKEND = 'django_ses.SESBackend'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']

STORAGES_S3BOTO_MULTI = {
    'media' : {
        'AWS_ACCESS_KEY_ID' : os.environ['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_ACCESS_KEY' : os.environ['AWS_SECRET_KEY'],
        'AWS_STORAGE_BUCKET_NAME' : 'media.ama.io',
        'AWS_S3_SECURE_URLS' : False,
        'AWS_S3_CUSTOM_DOMAIN' : "media.ama.io",
        'AWS_QUERYSTRING_AUTH' : False
    },
    'static' : {
        'AWS_ACCESS_KEY_ID' : os.environ['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_ACCESS_KEY' : os.environ['AWS_SECRET_KEY'],
        'AWS_STORAGE_BUCKET_NAME' : 'static.ama.io',
        'AWS_S3_SECURE_URLS' : False,
        'AWS_S3_CUSTOM_DOMAIN' : "static.ama.io",
        'AWS_QUERYSTRING_AUTH' : False,
        'AWS_LOCATION' : os.environ['PWD'].split("/")[-2],
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack_cloudsearch.cloudsearch_backend.CloudsearchSearchEngine',
        'AWS_ACCESS_KEY_ID' : os.environ['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_KEY' : os.environ['AWS_SECRET_KEY'],
        'IP_ADDRESS': '0.0.0.0',
        'SEARCH_DOMAIN_PREFIX': 'ama',
        #'SEARCH_DOMAIN_PREFIX': 'optional string to namespace your search domain with; defaults to haystack'
        #'MAX_SPINLOCK_TIME': 60*60,  # number of seconds before processing spinlocks give up
        #'PREPARE_SILENTLY': False, # If False, raise ValidationError if preparation of uploads fails.
                                    # If True, continue with upload
        #'REGION': 'us-east-1', # The region you want to create the search domain in. Defaults to 'us-east-1'
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

DEBUG = (os.environ.get("DEBUG", "FALSE") == "TRUE")
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

for host in os.environ.get("ALLOWED_HOSTS", "").split():
    ALLOWED_HOSTS += [host]
