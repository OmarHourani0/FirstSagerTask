"""
URL configuration for task1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from task1 import views
from django.contrib.auth import views as auth_views
from .views import danger, drone_flight_path, drone_list, drones_nearby



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/', views.hello_world),
    # path('', views.hello_world),
    path('health/', views.health_check),
    path('project/', views.name),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('data/', views.drone_data_list),
    path('nearby-drones/', drones_nearby, name='nearby_drones'),
    path('drone-list/', drone_list, name='drone_list'),
    path('danger-list/', danger, name='danger_list'),
    path('api/flight-path/<str:drone_id>/', views.drone_flight_path, name='drone_flight_path'),
    path('api/all-flight-paths/', views.all_drone_paths),
    path('drone-map/', views.drone_map, name='drone_map'),
    path('api/<str:drone_id_and_fields>/', views.dynamic_drone_api, name='dynamic_drone_api'),
    path('drone-query/', views.dynamic_drone_query_page, name='drone_query'),
]


