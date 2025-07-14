Usage
=====

To use the project you need to do the following:
- After doing all the setup steps you can access the Django application by navigating to `http://localhost:8000` in your web browser.
- The you can access all the pages of the application using APIs that are listed below:

1. **Authentication and Dashboards**:

- `/`  
  Login page

- `/data/`  
  Dashboard displaying real-time data for all drones (login required)

2. **Visualization and Query Tools**:

- `/drone-map/`  
  Interactive map showing real-time drone positions

- `/drone-query/`  
  Custom telemetry data queries per drone

3. **Filtered Data Views**:

- `/drone-list/`  
  List of all drone IDs with coordinates

- `/nearby-drones/`  
  Drones located within 5 km of the reference point (31.000, 39.000)

- `/danger-list/`  
  List of drones marked with a danger classification and explanation

4. **API Endpoints**:

- `/api/flight-path/<drone_id>/`  
  Returns the full flight path and current position of the specified drone

- `/api/all-flight-paths/`  
  Returns flight paths and positions of all drones


5. **Custom Query Format**:

To extract specific fields from a drone, navigate to `/drone-query/` and enter a string in the following format::
    
    'drone009-GEAR-HEIGHT-VERTICAL_SPEED-HEIGHT-ELEVATION-CLASSIFICATION'

- The first token is the `drone_id` (required)
- All other tokens correspond to telemetry fields you wish to retrieve (dash `-` separated)


6. **Available Data Fields**:

a. **Position and Motion**:

- `latitude`
- `longitude`
- `elevation`
- `height`
- `height_limit`
- `home_distance`
- `horizontal_speed`
- `vertical_speed`
- `wind_speed`
- `wind_direction`

b. **Status Flags and Modes**:

- `gear`
- `is_near_area_limit`
- `is_near_height_limit`
- `rc_lost_action`
- `rid_state`
- `rth_altitude`

c. **Storage**:

- `storage_total`
- `storage_used`

d. **Flight Summary**:

- `total_flight_distance`
- `total_flight_sorties`
- `total_flight_time`

e. **Miscellaneous**:

- `track_id`
- `classification`
- `timestamp`
