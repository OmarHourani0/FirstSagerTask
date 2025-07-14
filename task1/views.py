from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import model_to_dict
import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from droneData.models import DroneData

project_name = settings.PROJECT_NAME


# ---------- SHARED UTILITY ----------
def get_drone_geojson(drone_id):
    """
    Generate a GeoJSON LineString of the flight path for a given drone.

    Args:
        drone_id (str or int): The ID of the drone to fetch coordinates for.

    Returns:
        dict or None: GeoJSON feature containing drone flight path, or None if no data.
    """
    
    points = DroneData.objects.filter(drone_id=drone_id).order_by(
        'timestamp').values('longitude', 'latitude', 'timestamp')
    if not points.exists():
        return None

    return {
        "type": "Feature",
        "properties": {
            "drone_id": drone_id,
            "start_time": points.first()['timestamp'],
            "end_time": points.last()['timestamp'],
            "point_count": points.count()
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[p['longitude'], p['latitude']] for p in points]
        }
    }


# ---------- WEB VIEWS ----------

def asgi_test(request):
    """
    Render a test page for WebSocket communication.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered test page.
    """
    
    return render(request, 'websocket_test.html')


@login_required
def websocket_data_view(request):
    """
    Render the WebSocket data page with initial drone data.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered template with initial drone data.
    """
    
    latest = DroneData.objects.order_by('drone_id', '-timestamp').distinct('drone_id')
    data = [model_to_dict(d) for d in latest]
    return render(request, "websocket_data.html", {"initial_data": data})


@login_required
def drones_nearby(request):
    """
    Display drones whose home distance is less than or equal to 5km.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered template with nearby drones list.
    """
    
    try:
        data = DroneData.objects.order_by('-drone_id').values(
            'drone_id', 'longitude', 'latitude', 'home_distance')
        drones = [
            {
                "drone_id": d['drone_id'],
                "latitude": d['latitude'],
                "longitude": d['longitude'],
                "distance_km": round(d['home_distance'], 3)
            }
            for d in data if d['home_distance'] <= 5
        ]
    except Exception as e:
        traceback.print_exc()
        return render(request, "error.html", {"error": str(e)})

    return render(request, "nearby_drones.html", {"nearby_drones": drones})


@login_required
def danger(request):
    """
    Display drones flagged as dangerous (i.e., not classified as 'All Good').

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with dangerous drone classifications.
    """
    
    data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values('drone_id', 'classification')
    return render(request, 'danger.html', {'danger_list': data})


@login_required
def drone_flight_path_page(request, drone_id):
    """
    Render a page showing the drone flight path.

    Args:
        request (HttpRequest): Incoming HTTP request.
        drone_id (str): ID of the drone.

    Returns:
        HttpResponse: Rendered flight path page.
    """
    
    return render(request, 'drone_path.html', {'drone_id': drone_id})


@login_required
def all_drone_paths_page(request):
    """
    Render a page to view all drone flight paths.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with all flight paths.
    """
    
    return render(request, 'all_paths.html')


@login_required
def dynamic_drone_query_page(request):
    """
    Render a dynamic query page for retrieving custom drone data.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered dynamic query page.
    """
    
    return render(request, 'dynamic_drone_query.html')


@login_required
def drone_map(request):
    """
    Render a page with a map showing drone positions.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered map page.
    """
    
    return render(request, 'drone_map.html')


@login_required
def drone_list(request):
    """
    Render a list of drones with their coordinates.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered drone list page.
    """
    
    data = DroneData.objects.order_by('-drone_id').values('drone_id', 'latitude', 'longitude')
    return render(request, 'drone_list.html', {'drone_list': data})


def hello_world(request):
    """
    Render a simple hello world page.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered hello page.
    """
    return render(request, 'hello.html')


def name(request):
    return HttpResponse(f"Project is called {project_name}!")


def signup(request):
    """
    Handle user signup and render the registration form.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Redirect on success or render signup form.
    """
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def drone_data_list(request):
    """
    Render a list of all drone data entries.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered drone data list.
    """
    
    data = DroneData.objects.order_by('drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})


# ---------- API VIEWS ----------

@extend_schema(summary="Health Check", responses={200: str})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health_check(request):
    """
    Simple health check endpoint.

    Args:
        request (Request): Incoming API request.

    Returns:
        Response: "OK" message.
    """
    
    return Response("OK")


@extend_schema(summary="Project Name")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def name(request):
    """
    Return the name of the project.

    Args:
        request (Request): Incoming API request.

    Returns:
        Response: JSON containing project name.
    """
    
    return Response({"project_name": project_name})

@extend_schema(summary="Drone Data List")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_data_list(request):
    """
    Render the full list of drone data (same as web view).

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered data list.
    """
    
    data = DroneData.objects.order_by('drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})


@extend_schema(summary="Nearby Drones")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drones_nearby(request):
    """
    Return drones within 5km of their home location.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered list of nearby drones.
    """
    
    nearby_drones = []
    try:
        data = DroneData.objects.order_by('-drone_id').values('drone_id', 'longitude', 'latitude', 'home_distance')
        for drone in data:
            if drone['home_distance'] <= 5:
                nearby_drones.append({
                    "drone_id": drone['drone_id'],
                    "latitude": drone['latitude'],
                    "longitude": drone['longitude'],
                    "distance_km": round(drone['home_distance'], 3)
                })
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})
    return render(request, "nearby_drones.html", {"nearby_drones": nearby_drones})


@extend_schema(summary="Dangerous Drones")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def danger(request):
    """
    Return list of drones flagged as dangerous.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered danger classification page.
    """
    
    data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values('drone_id', 'classification')
    return render(request, 'danger.html', {'danger_list': data})


@extend_schema(summary="Flight Path GeoJSON")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_flight_path(request, drone_id):
    """
    Return flight path GeoJSON of a specific drone.

    Args:
        request (Request): Incoming API request.
        drone_id (str): ID of the drone.

    Returns:
        Response: GeoJSON LineString or 404 if not found.
    """
    
    geojson = get_drone_geojson(drone_id)
    if not geojson:
        return Response({"error": "No data found."}, status=404)
    return Response(geojson)


@extend_schema(summary="All Drone Paths GeoJSON")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_drone_paths(request):
    """
    Return GeoJSON FeatureCollection for all drone flight paths.

    Args:
        request (Request): Incoming API request.

    Returns:
        Response: GeoJSON with all drone paths.
    """
    
    features = []
    ids = DroneData.objects.values_list('drone_id', flat=True).distinct()
    for drone_id in ids:
        g = get_drone_geojson(drone_id)
        if g:
            features.append(g)
    return Response({"type": "FeatureCollection", "features": features})


@extend_schema(summary="Dynamic Drone Field API")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dynamic_drone_api(request, drone_id_and_fields):
    """
    Dynamically return selected fields for a specific drone.

    Args:
        request (Request): Incoming API request.
        drone_id_and_fields (str): Drone ID followed by field names separated by hyphens.

    Returns:
        Response: JSON object with requested fields or error.
    """
    
    try:
        parts = drone_id_and_fields.split('-')
        drone_id, fields = parts[0], parts[1:]
        
        field_map = {
            "TIMESTAMP": "timestamp", "LATITUDE": "latitude", "LONGITUDE": "longitude",
            "ELEVATION": "elevation", "HEIGHT": "height", "HEIGHT_LIMIT": "height_limit",
            "HOME_DISTANCE": "home_distance", "HORIZONTAL_SPEED": "horizontal_speed",
            "VERTICAL_SPEED": "vertical_speed", "WIND_SPEED": "wind_speed",
            "WIND_DIRECTION": "wind_direction", "GEAR": "gear",
            "NEAR_AREA_LIMIT": "is_near_area_limit", "NEAR_HEIGHT_LIMIT": "is_near_height_limit",
            "RC_LOST_ACTION": "rc_lost_action", "RID_STATE": "rid_state",
            "RTH_ALTITUDE": "rth_altitude", "STORAGE_TOTAL": "storage_total",
            "STORAGE_USED": "storage_used", "TOTAL_FLIGHT_DISTANCE": "total_flight_distance",
            "TOTAL_FLIGHT_SORTIES": "total_flight_sorties", "TOTAL_FLIGHT_TIME": "total_flight_time",
            "TRACK_ID": "track_id", "CLASSIFICATION": "classification"
        }

        selected_fields = ['drone_id'] + [field_map[f.upper()] for f in fields if f.upper() in field_map]

        drone = DroneData.objects.filter(drone_id=drone_id).order_by('-drone_id').values(*selected_fields).first()
        if not drone:
            return Response({'error': 'Drone not found'}, status=404)
        return Response(drone)

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@extend_schema(summary="Dynamic Drone Query Page")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dynamic_drone_query_page(request):
    """
    Render the dynamic drone query page for API.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered template.
    """
    
    return render(request, 'dynamic_drone_query.html')


@extend_schema(summary="Drone Map Page")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_map(request):
    """
    Render a map page showing all drones.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered map page.
    """
    
    return render(request, 'drone_map.html')


@extend_schema(summary="Drone List")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_list(request):
    """
    Render a list of drones with basic position data.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered drone list.
    """
    
    data = DroneData.objects.order_by('-drone_id').values('drone_id', 'latitude', 'longitude')
    return render(request, 'drone_list.html', {'drone_list': data})


@extend_schema(summary="Hello World Page")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello_world(request):
    return render(request, 'hello.html')


@extend_schema(summary="ASGI WebSocket Test")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def asgi_test(request):
    return render(request, 'websocket_test.html')


@extend_schema(summary="WebSocket Initial Data View")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def websocket_data_view(request):
    """
    Render WebSocket page with initial drone data.

    Args:
        request (Request): Incoming API request.

    Returns:
        HttpResponse: Rendered page with JSON-initialized template.
    """
    
    latest_per_drone = DroneData.objects.order_by('drone_id', '-timestamp').distinct('drone_id')
    data_for_template = [model_to_dict(d) for d in latest_per_drone]
    return render(request, "websocket_data.html", {"initial_data": data_for_template})
