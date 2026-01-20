from django.core.cache import cache
from django.http import HttpResponse
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/question/') and request.method == 'POST':
            user_ip = request.META.get('REMOTE_ADDR')
            key = f'rate_limit_{user_ip}'
            
            # Get the current timestamp
            now = time.time()
            
            # Get the list of request timestamps for this IP
            requests = cache.get(key, [])
            
            # Remove timestamps older than 1 minute
            requests = [req for req in requests if now - req < 60]
            
            # If more than 10 requests in the last minute, return 429
            if len(requests) >= 10:
                return HttpResponse('Too Many Requests', status=429)
            
            # Add current timestamp and save
            requests.append(now)
            cache.set(key, requests, 60)

        return self.get_response(request)