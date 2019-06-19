import math
'''
Based on https://stackoverflow.com/questions/238260/how-to-calculate-the-bounding-box-for-a-given-lat-lng-location
By Federico A Ramponi

and 

https://stackoverflow.com/questions/1648917/given-a-latitude-and-longitude-and-distance-i-want-to-find-a-bounding-box
By Ted

Create a 5km bounding box from a center point coordinate using lat/long

DePaul CDM coordinates provided by Google Maps: 41.8784523,-87.6277754
'''

# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0


# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi


# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis 
WGS84_b = 6356752.3  # Minor semiaxis 

# Earth radius at a given latitude, according to the WGS-84 ellipsoid
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt((An*An + Bn*Bn)/(Ad*Ad + Bd*Bd))

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def WGS84_Box(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    assert halfSideInKm > 0
    assert latitudeInDegrees >= -90.0 and latitudeInDegrees  <= 90.0
    assert longitudeInDegrees >= -180.0 and longitudeInDegrees <= 180.0

    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    # Gives you the radians for each lat, long line
    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius
    
    return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))