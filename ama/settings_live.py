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

INSTALLED_APPS += ('storages',)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = "ama.io"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False
