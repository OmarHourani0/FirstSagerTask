from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from task1.views import (
    # HTML views
    name, signup, drone_data_list, drone_list, danger,
    drone_flight_path_page, all_drone_paths_page, drone_map,
    dynamic_drone_query_page, asgi_test, websocket_data_view, drones_nearby,
    hello_world,

    # API views
    health_check, drone_flight_path, all_drone_paths, dynamic_drone_api
)

schema_view = get_schema_view(
    openapi.Info(
        title="My Django API",
        default_version='v1',
        description="API documentation for my Django project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin 
    path('admin/', admin.site.urls),
    
    # Auth
    path('', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    
    # HTML PAGES
    path('health/', health_check),
    path('project/', name),
    path('data/', drone_data_list),
    path('nearby-drones/', drones_nearby, name='nearby_drones'),
    path('drone-list/', drone_list, name='drone_list'),
    path('danger-list/', danger, name='danger_list'),
    path('drone-map/', drone_map, name='drone_map'),
    path('drone-query/', dynamic_drone_query_page, name='drone_query'),
    path('api/all-flight-paths/', all_drone_paths),
    
    
    # SWAGGER RELATED STUFF
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # WEBSOCKET APIs DO NOT TOUCH
    path('api/drone/<str:drone_id_and_fields>/',
         dynamic_drone_api, name='dynamic_drone_api'),
    path('api/flight-path/<str:drone_id>/',
         drone_flight_path, name='drone_flight_path'),
    path('asgi/', asgi_test, name='asgi_test'),
    path('websocket-data/', websocket_data_view, name='websocket_data'),
] 

