# from django.shortcuts import render
# from django.http import HttpResponse
# from django.conf import settings
# from droneData.models import DroneData
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from droneData.classifiers import haversine
# from django.http import JsonResponse
# from django.forms.models import model_to_dict
# from django.core.serializers.json import DjangoJSONEncoder
# import json
# import traceback
# # api_views.py (or just modify views.py)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from droneData.models import DroneData
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from drf_spectacular.utils import extend_schema
# from droneData.serializers import DroneDataSerializer  # You’ll need to define this


# project_name = settings.PROJECT_NAME


# def asgi_test(request):
#     return render(request, 'websocket_test.html')


# @login_required
# def websocket_data_view(request):
#     # get one latest-per-drone
#     latest_per_drone = (
#         DroneData.objects
#         .order_by('drone_id', '-timestamp')
#         .distinct('drone_id')
#     )
#     data_for_template = [model_to_dict(d) for d in latest_per_drone]
#     return render(request, "websocket_data.html", {
#         "initial_data": data_for_template
#     })


# @login_required
# def drones_nearby(request):
#     nearby_drones = []
#     try:
#         data = DroneData.objects.order_by('-drone_id').values(
#             'drone_id', 'longitude', 'latitude', 'home_distance',
#         )
#         print("Found drone IDs:", list(data.values_list('drone_id', flat=True)))

#         for drone in data:
#             try:
#                 if drone['home_distance'] <= 5:
#                     print(f"Adding {drone['drone_id']} to nearby list")
#                     nearby_drones.append({
#                         "drone_id": drone['drone_id'],
#                         "latitude": drone['latitude'],
#                         "longitude": drone['longitude'],  # Check field name!
#                         "distance_km": round(drone['home_distance'], 3)
#                     })
#             except KeyError as ke:
#                 print(f"[KeyError] Missing key in drone data: {ke}")
#                 continue
#             except Exception as e:
#                 print(f"[Drone Loop Error] {e}")
#                 traceback.print_exc()
#                 continue

#     except Exception as e:
#         print("[Top-level Error in drones_nearby]")
#         traceback.print_exc()
#         return render(request, "error.html", {"error": str(e)})

#     return render(request, "nearby_drones.html", {
#         "nearby_drones": nearby_drones
#     })


# @login_required
# def danger(request):
#     data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values(
#         'drone_id', 'classification',
#     )
#     print("DANGEROUS DRONES:")
#     for d in data:
#         print(d)
#     return render(request, 'danger.html', {
#         'danger_list': data,
#     })


# @login_required
# def drone_flight_path(request, drone_id):
#     # Get all positions for the drone ordered by time
#     points = DroneData.objects.filter(drone_id=drone_id).order_by(
#         'timestamp').values('longitude', 'latitude', 'timestamp')

#     # If no data found, return a 404
#     if not points.exists():
#         return JsonResponse({"error": "No data found for drone."}, status=404)

#     # Construct GeoJSON LineString Feature
#     geojson = {
#         "type": "Feature",
#         "properties": {
#             "drone_id": drone_id,
#             "start_time": points.first()['timestamp'],
#             "end_time": points.last()['timestamp'],
#             "point_count": points.count()
#         },
#         "geometry": {
#             "type": "LineString",
#             "coordinates": [
#                 [point['longitude'], point['latitude']] for point in points
#             ]
#         }
#     }
#     return JsonResponse(geojson)


# @login_required
# def dynamic_drone_api(request, drone_id_and_fields):
#     try:
#         parts = drone_id_and_fields.split('-')
#         drone_id = parts[0]
#         requested_fields = parts[1:]

#         # Map friendly names to actual model field names
#         field_map = {
#             # Core identifiers
#             "TIMESTAMP": "timestamp",

#             # Position & motion
#             "LATITUDE": "latitude",
#             "LONGITUDE": "longitude",
#             "ELEVATION": "elevation",
#             "HEIGHT": "height",
#             "HEIGHT_LIMIT": "height_limit",
#             "HOME_DISTANCE": "home_distance",
#             "HORIZONTAL_SPEED": "horizontal_speed",
#             "VERTICAL_SPEED": "vertical_speed",
#             "WIND_SPEED": "wind_speed",
#             "WIND_DIRECTION": "wind_direction",

#             # Status flags & modes
#             "GEAR": "gear",
#             "NEAR_AREA_LIMIT": "is_near_area_limit",
#             "NEAR_HEIGHT_LIMIT": "is_near_height_limit",
#             "RC_LOST_ACTION": "rc_lost_action",
#             "RID_STATE": "rid_state",
#             "RTH_ALTITUDE": "rth_altitude",

#             # Storage
#             "STORAGE_TOTAL": "storage_total",
#             "STORAGE_USED": "storage_used",

#             # Flight summary
#             "TOTAL_FLIGHT_DISTANCE": "total_flight_distance",
#             "TOTAL_FLIGHT_SORTIES": "total_flight_sorties",
#             "TOTAL_FLIGHT_TIME": "total_flight_time",

#             # Misc
#             "TRACK_ID": "track_id",
#             "CLASSIFICATION": "classification"
#         }

#         selected_fields = ['drone_id']  # always include drone_id
#         for field in requested_fields:
#             if field.upper() in field_map:
#                 selected_fields.append(field_map[field.upper()])

#         # Fetch the latest entry for that drone
#         if len(selected_fields) == 1:
#             drone = DroneData.objects.filter(
#                 drone_id=drone_id).order_by('-drone_id').values().first()
#         else:
#             drone = DroneData.objects.filter(drone_id=drone_id).order_by(
#                 '-drone_id').values(*selected_fields).first()

#         if not drone:
#             return JsonResponse({'error': 'Drone not found'}, status=404)

#         return JsonResponse(drone)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)


# @login_required
# def dynamic_drone_query_page(request):
#     return render(request, 'dynamic_drone_query.html')


# @login_required
# def all_drone_paths(request):
#     drone_ids = DroneData.objects.values_list('drone_id', flat=True).distinct()
#     features = []

#     for drone_id in drone_ids:
#         points = DroneData.objects.filter(drone_id=drone_id).order_by(
#             'timestamp').values('longitude', 'latitude', 'timestamp')
#         if not points.exists():
#             continue

#         coords = [[p['longitude'], p['latitude']] for p in points]

#         features.append({
#             "type": "Feature",
#             "properties": {
#                 "drone_id": drone_id,
#                 "start_time": points.first()['timestamp'],
#                 "end_time": points.last()['timestamp'],
#             },
#             "geometry": {
#                 "type": "LineString",
#                 "coordinates": coords
#             }
#         })

#     return JsonResponse({
#         "type": "FeatureCollection",
#         "features": features
#     })


# @login_required
# def drone_map(request):
#     return render(request, 'drone_map.html')


# @login_required
# def drone_list(request):
#     data = DroneData.objects.order_by('-drone_id').values(
#         'drone_id', 'latitude', 'longitude'
#     )
#     return render(request, 'drone_list.html', {'drone_list': data})


# def hello_world(request):
#     return render(request, 'hello.html', {})


# @extend_schema(
#     summary="Health Check Endpoint",
#     responses={200: str}
# )
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def health_check(request):
#     return Response("OK")


# def name(request):
#     return HttpResponse(f"Project is called {project_name}!")


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # redirect to login after successful signup
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


# @login_required
# def drone_data_list(request):
#     data = DroneData.objects.order_by('drone_id')
#     return render(request, 'data_list.html', {'drone_data_list': data})


# ✅ REFACTORED VIEWS

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
    return render(request, 'websocket_test.html')


@login_required
def websocket_data_view(request):
    latest = DroneData.objects.order_by('drone_id', '-timestamp').distinct('drone_id')
    data = [model_to_dict(d) for d in latest]
    return render(request, "websocket_data.html", {"initial_data": data})


@login_required
def drones_nearby(request):
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
    data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values('drone_id', 'classification')
    return render(request, 'danger.html', {'danger_list': data})


@login_required
def drone_flight_path_page(request, drone_id):
    return render(request, 'drone_path.html', {'drone_id': drone_id})


@login_required
def all_drone_paths_page(request):
    return render(request, 'all_paths.html')


@login_required
def dynamic_drone_query_page(request):
    return render(request, 'dynamic_drone_query.html')


@login_required
def drone_map(request):
    return render(request, 'drone_map.html')


@login_required
def drone_list(request):
    data = DroneData.objects.order_by('-drone_id').values('drone_id', 'latitude', 'longitude')
    return render(request, 'drone_list.html', {'drone_list': data})


def hello_world(request):
    return render(request, 'hello.html')


def name(request):
    return HttpResponse(f"Project is called {project_name}!")


def signup(request):
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
    data = DroneData.objects.order_by('drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})


# ---------- API VIEWS ----------

@extend_schema(summary="Health Check", responses={200: str})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health_check(request):
    return Response("OK")


@extend_schema(summary="Project Name")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def name(request):
    return Response({"project_name": project_name})

@extend_schema(summary="Drone Data List")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_data_list(request):
    data = DroneData.objects.order_by('drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})


@extend_schema(summary="Nearby Drones")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drones_nearby(request):
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
    data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values('drone_id', 'classification')
    return render(request, 'danger.html', {'danger_list': data})


@extend_schema(summary="Flight Path GeoJSON")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_flight_path(request, drone_id):
    geojson = get_drone_geojson(drone_id)
    if not geojson:
        return Response({"error": "No data found."}, status=404)
    return Response(geojson)


@extend_schema(summary="All Drone Paths GeoJSON")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_drone_paths(request):
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
    return render(request, 'dynamic_drone_query.html')


@extend_schema(summary="Drone Map Page")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_map(request):
    return render(request, 'drone_map.html')


@extend_schema(summary="Drone List")
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drone_list(request):
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
    latest_per_drone = DroneData.objects.order_by('drone_id', '-timestamp').distinct('drone_id')
    data_for_template = [model_to_dict(d) for d in latest_per_drone]
    return render(request, "websocket_data.html", {"initial_data": data_for_template})
