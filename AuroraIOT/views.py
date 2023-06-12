from django.shortcuts import HttpResponse

def homepage(request):
    return HttpResponse("<h1>AuroraIOT is Running</h1>")