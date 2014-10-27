EARTH_RADIUS_km = 6373
WEATHER_PROVIDER_NAME = 'noaa_wavewatch_model_3'
__author__ = 'SKuptsov'

from grib_api.gribapi import *
from admin.models import *
from datetime import datetime
from datetime import timedelta
import math


def createMarineWeatherRecord(spot_id, date, time, nearest_grid_lat, nearest_grid_long,
                              nearest_distance, param_type_name, param_value, weather_provider_name):
    try:
        spot = Spot.objects.get(id=spot_id)

        marineWeatherProvider = MarineWeatherProvider.objects.get(name=weather_provider_name)
        param_type_mapping = MarineWeatherPrmTypePrvdrMapping.objects.get(provider_param_name=param_type_name,
                                                                          marine_weather_provider=marineWeatherProvider)
        param_type = param_type_mapping.marine_weather_param_type

        if MarineWeatherHistory.objects.filter(spot=spot, date=date, time=time, param_type=param_type,
                                               marineWeatherProvider=marineWeatherProvider).exists() and param_value is not None:
            record = MarineWeatherHistory.objects.get(spot=spot, date=date, time=time, param_type=param_type,
                                                      marineWeatherProvider=marineWeatherProvider)

            if record.id == 13717 :
                pass
            record.nearest_grid_lat = nearest_grid_lat
            record.nearest_grid_long = nearest_grid_long
            record.nearest_distance = nearest_distance
            record.param_value = param_value
        else:
            record = MarineWeatherHistory(spot=spot, date=date, time=time, nearest_grid_lat=nearest_grid_lat,
                                          nearest_grid_long=nearest_grid_long, nearest_distance=nearest_distance,
                                          param_type=param_type, param_value=param_value,
                                          marineWeatherProvider=marineWeatherProvider)
        record.save()

    except Exception, e:
        print str(e)


def find_nearest_value(gid, lat, lon):
    nearest = grib_find_nearest(gid, lat, lon)[0]
    if nearest.value == 9999:
        nearest.value = None
        #print lat, lon
    return nearest

def distance_on_unit_sphere_km(lat1, long1, lat2, long2):


    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )


    return arc* EARTH_RADIUS_km


def iterateWithGribFileAndSpotIterator(grib_file_path, next_spot_iterator):
    f = open(grib_file_path)

    while 1:
        gid = grib_new_from_file(f)
        if isinstance(gid, int) == False:
            break

        dataDate = grib_get(gid, 'dataDate')
        hour = grib_get(gid, 'forecastTime')

        date_object = datetime.strptime(str(dataDate), '%Y%m%d')
        date_object = date_object + timedelta(hours=hour)

        if date_object != datetime.strptime('20131201', '%Y%m%d') :
            break

        time_object = datetime.strptime(str(int(hour) % 24), '%H')

        print(date_object)

        print(time_object)

        param_type_name = grib_get(gid, 'shortNameECMF')

        for spot in next_spot_iterator:

            try:
                nearest = find_nearest_value(gid, spot.latitude, spot.longitude)

                #if nearest.value != None:
                createMarineWeatherRecord(spot.id, date_object, time_object, nearest.lat, nearest.lon,
                                          nearest.distance,
                                          param_type_name, nearest.value,
                                          WEATHER_PROVIDER_NAME)
                #else:
                #    print("Found none value")
            except GribInternalError, e:
                pass
                #print(e)

        grib_release(gid)

    f.close()


class spot_iter():
    def __iter__(self):
        return self

    def next(self):
        spot = Spot.objects.all()
        return spot


def test():
    dir = 'test/data/201312/hs_loc'
    for filename in os.listdir(dir):
        print("Current filename " + filename)
        iterateWithGribFileAndSpotIterator(dir + "/" + filename, Spot.objects.all())


test()








