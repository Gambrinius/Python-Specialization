from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET,  require_POST


@require_GET
def simple_route(request):
    return HttpResponse()


def slug_route(request, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    try:
        sum = str(int(a) + int(b))
    except ValueError:
        return HttpResponseNotFound()

    return HttpResponse(sum)


@require_GET
def sum_get_method(request):
    a, b = request.GET.get('a', ''), request.GET.get('b', '')
    if a and b:
        try:
            sum = str(int(a) + int(b))
        except ValueError:
            return HttpResponseBadRequest()

        return HttpResponse(sum)
    else:
        return HttpResponseBadRequest()


@require_POST
def sum_post_method(request):
    a, b = request.POST.get('a', ''), request.POST.get('b', '')
    if a and b:
        try:
            sum = str(int(a) + int(b))
        except ValueError:
            return HttpResponseBadRequest()

        return HttpResponse(sum)
    else:
        return HttpResponseBadRequest()
