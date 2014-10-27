__author__ = 'SKuptsov'

MAGICSEAWEED_COM = "http://magicseaweed.com/"

from selenium import webdriver
import time
from admin.models import *


def updateSpotCoord(spot_name, latitude, longitude):
    if Spot.objects.filter(spot_name=spot_name).exists():
        spot = Spot.objects.get(spot_name=spot_name)
        spot.longitude = longitude
        spot.latitude = latitude
        spot.save(update_fields=['longitude', 'latitude'])

startPoint = "/Antarctic-Peninsula-Surf-Forecast/94/"

def updateCoordinates():
    driver = webdriver.Firefox()

    isStartPoint = False
    for link in MagicSeaWeedLink.objects.all():

        if(link.link == MAGICSEAWEED_COM+startPoint):
            isStartPoint = True

        if isStartPoint is True:
            #time.sleep(5)
            driver.get(link.link)

            i = 0
            while True:
                try:
                    spot_title = driver.execute_script("return googleMapFrame.markerArrays.spot[" + str(i) + "].title")
                    if i  == 67:
                        k=0
                    spot_latitude = driver.execute_script(
                        "return googleMapFrame.markerArrays.spot[" + str(i) + "].position.k")
                    spot_longitude = driver.execute_script(
                        "return googleMapFrame.markerArrays.spot[" + str(i) + "].position.B")
                    updateSpotCoord(spot_title, spot_latitude, spot_longitude)
                    i += 1
                except Exception as e:
                    print(e)
                    break

    driver.close()


updateCoordinates()






