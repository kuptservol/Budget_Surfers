import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GonnaSurfServices.settings")

from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=200, unique=True)
    parent = models.BigIntegerField(blank=True, null=True)
    path = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return 'place_name: ' + self.name + ' parent: ' + str(self.parent)

    @classmethod
    def create(cls, name, parent):
        place = cls(name=name, parent=parent)
        return place


class Spot(models.Model):
    spot_name = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()
    place = models.ForeignKey(Place)

    def __unicode__(self):
        return str(self.spot_name)

    def __str__(self):
        return self.spot_name


class HttpService(models.Model):
    api_service_key = models.CharField(max_length=200)
    max_request_per_day = models.BigIntegerField()
    current_date = models.DateField(blank=True, null=True)
    max_request_per_second = models.IntegerField()
    base_url = models.CharField(max_length=200)
    current_request_per_day_number = models.BigIntegerField()


class PredefinedHttpServiceGetParams(models.Model):
    httpService = models.ForeignKey(HttpService)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class MagicSeaWeedLink(models.Model):
    link = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=200)
    entity_id = models.BigIntegerField()
    entity_str = models.CharField(max_length=200)

class MarineWeatherProvider(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)

class MarineWeatherParamType(models.Model):
    name = models.CharField(max_length = 50, null=True)
    description = models.CharField(max_length=200, null=True)
    unit_of_measure = models.CharField(max_length = 10)

class MarineWeatherHistory(models.Model):
    spot = models.ForeignKey(Spot)
    date = models.DateField()
    time = models.TimeField()
    nearest_grid_lat = models.FloatField()
    nearest_grid_long = models.FloatField()
    nearest_distance = models.FloatField()
    param_type = models.ForeignKey(MarineWeatherParamType)
    param_value = models.FloatField()
    marineWeatherProvider = models.ForeignKey(MarineWeatherProvider)

class MarineWeatherPrmTypePrvdrMapping(models.Model):
    marine_weather_param_type = models.ForeignKey(MarineWeatherParamType)
    marine_weather_provider = models.ForeignKey(MarineWeatherProvider)
    provider_param_name = models.CharField(max_length = 100, null=True)
    provider_param_id = models.IntegerField(null=True)
    provider_param_description = models.CharField(max_length=100, null=True)

