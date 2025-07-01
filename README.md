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
