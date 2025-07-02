from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from droneData.models import DroneData
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from droneData.classifiers import haversine
from django.http import JsonResponse


project_name = settings.PROJECT_NAME


@login_required
def drones_nearby(request):
    nearby_drones = []

    drone_ids = DroneData.objects.values_list('drone_id', flat=True).distinct()
    print("Found drone IDs:", list(drone_ids))

    for drone_id in drone_ids:
        try:
            drone = DroneData.objects.filter(
                drone_id=drone_id).latest('timestamp')
            print(
                f"Checking {drone.drone_id} with home_distance: {drone.home_distance}")
        except DroneData.DoesNotExist:
            continue

        if drone.home_distance <= 5:
            print(f"Adding {drone.drone_id} to nearby list")
            nearby_drones.append({
                "drone_id": drone.drone_id,
                "latitude": drone.latitude,
                "longitude": drone.longitude,
                "distance_km": round(drone.home_distance, 3)
            })

    return render(request, "nearby_drones.html", {
        "nearby_drones": sorted(nearby_drones, key=lambda x: x['drone_id'])
    })


@login_required
def danger(request):
    data = DroneData.objects.exclude(classification="All Good").order_by('-drone_id').values(
        'drone_id', 'classification',
    )
    print("DANGEROUS DRONES:")
    for d in data:
        print(d)
    return render(request, 'danger.html', {
        'danger_list': data,
    })


def drone_flight_path(request, drone_id):
    # Get all positions for the drone ordered by time
    points = DroneData.objects.filter(drone_id=drone_id).order_by(
        'timestamp').values('longitude', 'latitude', 'timestamp')

    # If no data found, return a 404
    if not points.exists():
        return JsonResponse({"error": "No data found for drone."}, status=404)

    # Construct GeoJSON LineString Feature
    geojson = {
        "type": "Feature",
        "properties": {
            "drone_id": drone_id,
            "start_time": points.first()['timestamp'],
            "end_time": points.last()['timestamp'],
            "point_count": points.count()
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [point['longitude'], point['latitude']] for point in points
            ]
        }
    }
    return JsonResponse(geojson)


def dynamic_drone_api(request, drone_id_and_fields):
    try:
        parts = drone_id_and_fields.split('-')
        drone_id = parts[0]
        requested_fields = parts[1:]

        # Map friendly names to actual model field names
        field_map = {
            # Core identifiers
            "TIMESTAMP": "timestamp",

            # Position & motion
            "LATITUDE": "latitude",
            "LONGITUDE": "longitude",
            "ELEVATION": "elevation",
            "HEIGHT": "height",
            "HEIGHT_LIMIT": "height_limit",
            "HOME_DISTANCE": "home_distance",
            "HORIZONTAL_SPEED": "horizontal_speed",
            "VERTICAL_SPEED": "vertical_speed",
            "WIND_SPEED": "wind_speed",
            "WIND_DIRECTION": "wind_direction",

            # Status flags & modes
            "GEAR": "gear",
            "NEAR_AREA_LIMIT": "is_near_area_limit",
            "NEAR_HEIGHT_LIMIT": "is_near_height_limit",
            "RC_LOST_ACTION": "rc_lost_action",
            "RID_STATE": "rid_state",
            "RTH_ALTITUDE": "rth_altitude",

            # Storage
            "STORAGE_TOTAL": "storage_total",
            "STORAGE_USED": "storage_used",

            # Flight summary
            "TOTAL_FLIGHT_DISTANCE": "total_flight_distance",
            "TOTAL_FLIGHT_SORTIES": "total_flight_sorties",
            "TOTAL_FLIGHT_TIME": "total_flight_time",

            # Misc
            "TRACK_ID": "track_id",
            "CLASSIFICATION": "classification"
        }

        selected_fields = ['drone_id']  # always include drone_id
        for field in requested_fields:
            if field.upper() in field_map:
                selected_fields.append(field_map[field.upper()])

        # Fetch the latest entry for that drone
        drone = DroneData.objects.filter(drone_id=drone_id).order_by(
            '-drone_id').values(*selected_fields).first()

        if not drone:
            return JsonResponse({'error': 'Drone not found'}, status=404)

        return JsonResponse(drone)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def dynamic_drone_query_page(request):
    return render(request, 'dynamic_drone_query.html')


def all_drone_paths(request):
    drone_ids = DroneData.objects.values_list('drone_id', flat=True).distinct()
    features = []

    for drone_id in drone_ids:
        points = DroneData.objects.filter(drone_id=drone_id).order_by(
            'timestamp').values('longitude', 'latitude', 'timestamp')
        if not points.exists():
            continue

        coords = [[p['longitude'], p['latitude']] for p in points]

        features.append({
            "type": "Feature",
            "properties": {
                "drone_id": drone_id,
                "start_time": points.first()['timestamp'],
                "end_time": points.last()['timestamp'],
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })


@login_required
def drone_map(request):
    return render(request, 'drone_map.html')


@login_required
def drone_list(request):
    data = DroneData.objects.order_by('-drone_id').values(
        'drone_id', 'latitude', 'longitude'
    )
    return render(request, 'drone_list.html', {'drone_list': data})


def hello_world(request):
    return render(request, 'hello.html', {})


def health_check(request):
    return HttpResponse("OK")


def name(request):
    return HttpResponse(f"Project is called {project_name}!")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to login after successful signup
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def drone_data_list(request):
    data = DroneData.objects.order_by('-drone_id')
    return render(request, 'data_list.html', {'drone_data_list': data})
