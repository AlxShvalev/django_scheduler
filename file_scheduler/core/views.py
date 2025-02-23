from django.http import HttpResponse


def index(request):
    return HttpResponse("<b>There will be something here.</b>")
