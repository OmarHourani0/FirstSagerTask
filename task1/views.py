from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from droneData.models import DroneData


project_name = settings.PROJECT_NAME


def hello_world(request):
    return render(request, 'hello.html', {})


def health_check(request):
    return HttpResponse("OK")

def nig(request):
    return HttpResponse("I hate NIGS")

def name(request):
    return HttpResponse(f"Project is called {project_name}!")

def drone_data_list(request):
    # Get latest 100 entries ordered by newest first
    data = DroneData.objects.all().order_by('-drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})
