from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
from django.conf import settings
from apiclient import discovery

#credentials = SignedJwtAssertionCredentials.from_json(settings.GOOGLE_KEY)
#http = httplib2.Http()
#credentials.refresh(http)
#http = credentials.authorize(http)

#service = discovery.build('analytics', 'v3', http=http)
service = {}
