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
        'LOCATION': 'ama.uxft7n.0001.use1.cache.amazonaws.com:11211',
    }
}

INSTALLED_APPS += ('storages',)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

DEFAULT_FILE_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'
STATICFILES_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_static'
EMAIL_BACKEND = 'django_ses.SESBackend'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'

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

AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
