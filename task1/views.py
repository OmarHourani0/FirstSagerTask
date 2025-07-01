from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from droneData.models import DroneData
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



project_name = settings.PROJECT_NAME


def hello_world(request):
    return render(request, 'hello.html', {})


def health_check(request):
    return HttpResponse("OK")

def nig(request):
    return HttpResponse("I hate NIGS")

def name(request):
    return HttpResponse(f"Project is called {project_name}!")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def drone_data_list(request):
    data = DroneData.objects.order_by('-drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})
