__author__ = 'SKuptsov'
from admin.models import *
import datetime
import admin
import time


class HttpService:
    global persistRequestPerDayStep
    persistRequestPerDayStep = 10

    def __init__(self, api_service_key):
        self.api_service_key = api_service_key
        if admin.models.HttpService.objects.filter(api_service_key=api_service_key).exists():
            service = admin.models.HttpService.objects.get(api_service_key=api_service_key)
            self.service = service
            self.max_request_per_day = service.max_request_per_day
            self.max_request_per_second = service.max_request_per_second
            self.base_url = service.base_url
            if datetime.date.today() == service.current_date:
                self.current_request_per_day_number = service.current_request_per_day_number
            else:
                self.current_request_per_day_number = 0
            self.minInterval = 1.0 / float(self.max_request_per_second)
            self.exists = True
            self.lastTimeCalled = [0.0]
            self.dayLimitExhausted = False
        else:
            self.exists = False

    def persistRequestPerDay(self, current_request_per_day_number):
        self.service.current_request_per_day_number = current_request_per_day_number
        self.service.current_date = datetime.date.today()
        self.service.save(update_fields=['current_request_per_day_number', 'current_date'])


    def executeAtFixedRate(self, executeMethod, **kwargs):
        elapsed = time.clock() - self.lastTimeCalled[0]
        leftToWait = self.minInterval - elapsed
        if leftToWait > 0:
            time.sleep(leftToWait)
            self.current_request_per_day_number += 1
            if self.current_request_per_day_number % persistRequestPerDayStep == 0:
                self.persistRequestPerDay(self.current_request_per_day_number)
            if self.current_request_per_day_number >= self.max_request_per_day:
                self.dayLimitExhausted = True
                raise NameError("Day limit on service key=" + self.api_service_key + " is exhausted")
            executeMethod(**kwargs)
        self.lastTimeCalled[0] = time.clock()

    def makeRequest(self, **kwargs):
        print("Request " + str(kwargs['argument']))

    def execute(self, **kwargs):
        self.executeAtFixedRate(self.makeRequest, **kwargs)


class HttpServiceFactory:
    services = {"worldweatheronline.marine": HttpService(api_service_key="worldweatheronline.marine"),
                "marineWeatherApi": HttpService(api_service_key="marineWeatherApi")}

    @staticmethod
    def getService(api_service_name):
        if HttpServiceFactory.services.__contains__(api_service_name) \
            and HttpServiceFactory.services[api_service_name].exists is True:
            return HttpServiceFactory.services[api_service_name]
        else:
            raise NameError('Defined http service ' + api_service_name + ' does not exists')


s = HttpServiceFactory.getService("worldweatheronline.marine")
for i in range(1, 21):
    s.execute(argument=i)



