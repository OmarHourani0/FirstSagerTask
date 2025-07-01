from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

project_name = settings.PROJECT_NAME


def hello_world(request):
    return render(request, 'hello.html', {})


def health_check(request):
    return HttpResponse("OK")

def nig(request):
    return HttpResponse("I hate NIGS")

def name(request):
    return HttpResponse(f"Project is called {project_name}!")
