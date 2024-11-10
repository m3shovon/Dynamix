from django.utils.deprecation import MiddlewareMixin
from .models import HitCounter

class HitCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Fetch the counter object or create it if it does not exist
        counter, created = HitCounter.objects.get_or_create(id=1)
        # Increment the count
        counter.count += 1
        # Save the updated count
        counter.save()