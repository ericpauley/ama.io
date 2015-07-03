from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
from django.conf import settings
from apiclient import discovery
import os
import json
try:
    data = json.load(open(os.path.join(settings.PROJECT_PATH, 'google.json')))
except:
    data = None

if data is not None:
    credentials = SignedJwtAssertionCredentials(data['client_email'], data['private_key'], "https://www.googleapis.com/auth/analytics.readonly")
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)

    service = discovery.build('analytics', 'v3', http=http)
else:
    service = {}
