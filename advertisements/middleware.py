from urllib.parse import parse_qs, urlencode


class QueryStringCleanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if ' ' in request.META.get('QUERY_STRING', ''):
            qs = parse_qs(request.META['QUERY_STRING'])
            clean_qs = {k.strip(): v for k, v in qs.items()}
            request.META['QUERY_STRING'] = urlencode(clean_qs, doseq=True)

        response = self.get_response(request)
        return response