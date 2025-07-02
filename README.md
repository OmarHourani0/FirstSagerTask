# First Sager Task

# PORT: 8000

# API LIST
1) / --> Login Page
2) /data --> Shows all the data of every drone
3) /nearby-drones --> Shows a list of drones that less than 5km away from the reference point which is {31.000, 39.000}
4) /drone-list --> Shows every drone_ID, Longitude, and Latitude
5) /danger-list --> Shows every drone that is marked with a "danger" flag and shows why it was flagged
6) /api/flight-path/<str:drone_id>/ --> Shows the flight path information and current location of drone (Put the drone ID in the URL, {drone001 - drone100})
7) /api/all-flight-paths/ --> Shows the flight path information and current location of every drone
8) /drone-map/ --> Interactive map that shows the locations of each drone as pings
9) /drone-query/ --> A page will come up where you can make custom queries. Instructions on the page should be clear. A custome query would look like this:
## {drone009-GEAR-HEIGHT-VERTICAL_SPEED-HEIGHT-ELEVATION-CLASSIFICATION}.
### {drone_id (required) - {any data from the list below seperated by a dash (-)}}

# Data Available for queries

## Position & motion
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

## Status flags & modes
"GEAR": "gear",
"NEAR_AREA_LIMIT": "is_near_area_limit",
"NEAR_HEIGHT_LIMIT": "is_near_height_limit",
"RC_LOST_ACTION": "rc_lost_action",
"RID_STATE": "rid_state",
"RTH_ALTITUDE": "rth_altitude",

## Storage
"STORAGE_TOTAL": "storage_total",
"STORAGE_USED": "storage_used",

## Flight summary
"TOTAL_FLIGHT_DISTANCE": "total_flight_distance",
"TOTAL_FLIGHT_SORTIES": "total_flight_sorties",
"TOTAL_FLIGHT_TIME": "total_flight_time",

## Misc
"TRACK_ID": "track_id",
"CLASSIFICATION": "classification"
"TIMESTAMP": "timestamp",    
