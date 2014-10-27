MAGICSEAWEED_COM = "http://magicseaweed.com/"
MAGICSEAWEED_ARCHIVE_COM = "http://web.archive.org/web/20140730031533/http://magicseaweed.com/"
START_CSS_SELECTOR = 'li.msw-base-chzn-ss select.msw-js-spotselect.msw-base-ss.chzn-done'
#START_CSS_SELECTOR = 'li.option-primary select.msw-js-breadcrumb-region.select2-offscreen'
__author__ = 'SKuptsov'

from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import Tag
from admin.models import *


def createPlace(placeName, parentPlaceName):
    if not Place.objects.filter(name=placeName).exists():
        if parentPlaceName is not None and Place.objects.filter(name=parentPlaceName).exists():
            parentPlace = Place.objects.get(name=parentPlaceName)
            newPlace = Place(name=placeName, parent=parentPlace.id)
            newPlace.save()
            newPlace.path = parentPlace.path + str(newPlace.id) + '/'
            newPlace.save(update_fields=['path'])
        else:
            newPlace = Place(name=placeName)
            newPlace.save()
            newPlace.path = '/' + str(newPlace.id) + '/'
            newPlace.save(update_fields=['path'])

        return newPlace
    else:
        return Place.objects.get(name=placeName)


def createSpotWithPlace(spotName, placeName, parentPlaceName):
    if not Spot.objects.filter(spot_name=spotName).exists():
        if Place.objects.filter(name=placeName).exists():
            place = Place.objects.get(name=placeName)
            spot = Spot(spot_name=spotName, longitude=0, latitude=0, place=place)
            spot.save()
        else:
            place = createPlace(placeName, parentPlaceName)
            spot = Spot(spot_name=spotName, longitude=0, latitude=0, place=place)
            spot.save()

        return spot
    else:
        return Spot.objects.get(spot_name=spotName)

def createNewMagicSeaWeed(link, entity_type, entity_id, entity_str):
    if not MagicSeaWeedLink.objects.filter(entity_type=entity_type, entity_id=entity_id).exists():
        magicSeaWeedLink = MagicSeaWeedLink(link=link, entity_type=entity_type, entity_id=entity_id, entity_str=entity_str)
        magicSeaWeedLink.save()



def insertNewPlaceSpots():
    global driver, html, css_soup, select, regions_list, placeList, region, region_name, subregions_list, subregion, placeMap, place, spot_list, spotPlace, placeName, parentPlaceName, spot
    driver = webdriver.Firefox()
    driver.get(MAGICSEAWEED_ARCHIVE_COM)
    html = driver.page_source
    css_soup = BeautifulSoup(html)
    select = css_soup.select(START_CSS_SELECTOR)
    if len(select) > 0:
        regions_list = select[0].contents
        placeList = []
        for region in regions_list:
            if isinstance(region, Tag):
                region_name = region.attrs['label']
                createPlace(region_name, None)

                subregions_list = region.contents
                for subregion in subregions_list:
                    if isinstance(subregion, Tag):
                        place = createPlace(subregion.contents[0], region_name)
                        placeName = subregion.contents[0]
                        path = subregion.attrs['value']
                        print(path)
                        print(placeName)
                        createNewMagicSeaWeed(MAGICSEAWEED_COM+path, "place", place.id, place.__str__())
                        placeMap = {"placeName": placeName, "placePath": path}
                        placeList.append(placeMap)

        startPoint = True

        for place in placeList:
            print(place['placePath'])
            #if place['placePath'] == '/Israel-Surf-Forecast/90/':
            #    startPoint = True
            #else:
            #    startPoint = False
            if startPoint is True:
                driver.get(MAGICSEAWEED_ARCHIVE_COM + place['placePath'])
                html = driver.page_source
                css_soup = BeautifulSoup(html)


                select = css_soup.select(START_CSS_SELECTOR)
                if len(select) > 1:
                    spot_list = select[1].contents
                    for spotPlace in spot_list:
                        if isinstance(spotPlace, Tag) and spotPlace.contents[0] != 'Surf Spot...':
                            placeName = spotPlace.attrs['label']
                            parentPlaceName = place['placeName']
                            for spot in spotPlace.contents:
                                if isinstance(spot, Tag):
                                    print(spot.contents[0])
                                    createSpotWithPlace(spot.contents[0], placeName, parentPlaceName)

    driver.close()


insertNewPlaceSpots()






