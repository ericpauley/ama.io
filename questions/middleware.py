from django.utils import timezone
from datetime import tzinfo, timedelta, datetime
import pytz

class TimezoneMiddleware(object):
    def process_request(self, request):
        try:
            timezone.activate(pytz.timezone(request.COOKIES['tzname']))
        except:
            timezone.deactivate()
