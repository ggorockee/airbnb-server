from django.http import JsonResponse


def health_check(request):
    resp = {
        "status": "active"
    }
    return JsonResponse(resp, status=200)