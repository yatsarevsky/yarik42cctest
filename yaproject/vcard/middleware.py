from .models import RequestStore


class RequestStoreWare:
    def process_request(self, request):
        r = RequestStore()
        r.host = request.get_host()
        r.path = request.get_full_path()
        r.save()
        return None
