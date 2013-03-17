from .models import RequestStore


class RequestStoreWare:
    def process_request(self, request):
        r = RequestStore()
        r.host = request.get_host()
        r.path = request.get_full_path()
        if '/request_store/' not in r.path:
            r.save()
        return None
