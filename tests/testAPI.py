import unittest
from unittest import mock

import pytest as pytest
from freezegun import freeze_time
from getWeather import GetWeather
from tests.mockData import API_RESPONSE_GET_CURRENT_WEATHER, API_RESPONSE_GET_DAILY_WEATHER


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.weatherApp = GetWeather()

    def testGetCurrentWeather(self):
        with mock.patch(
            "getWeather.GetWeather.callWeatherApi",
            return_value=API_RESPONSE_GET_CURRENT_WEATHER,
        ):
            weatherInfo = self.weatherApp.getCurrentWeather(longitude=34, latitude=95)

            assert weatherInfo.id == 627908
            assert weatherInfo.main.temp == 271.54
            assert weatherInfo.main.pressure == 1008
            assert weatherInfo.main.humidity == 56
            assert weatherInfo.name == "Hlybokaye"

    def testGetDailyWeather(self):
        with mock.patch(
            "getWeather.GetWeather.callWeatherApi",
            return_value=API_RESPONSE_GET_DAILY_WEATHER,
        ):
            weather = self.weatherApp.getDailyWeather(longitude=30, latitude=55)
            listDays = weather.daily
            dayOne = listDays[0]
            assert len(listDays) == 8
            assert dayOne.humidity == 37
            assert dayOne.pressure == 1007
            # test tempToCelsius
            minTemp = self.weatherApp.tempToCelsius(dayOne.temp.min)
            maxTemp = self.weatherApp.tempToCelsius(dayOne.temp.max)
            assert minTemp == -2.9
            assert maxTemp == 2.09

    def testCallWeatherApiFailure(self):
        with pytest.raises(Exception):
            self.weatherApp.callWeatherApi("ewe", {})

    @freeze_time("2021-02-03T21:53:00+00:00")
    def testGetDateTimes(self):
        """
        Test for getListOfDateTimesForPastFiveDays method
        """
        dateList = self.weatherApp.getListOfDateTimesForPastFiveDays()
        assert len(dateList) == 5
        assert dateList == [1612302780, 1612216380, 1612129980, 1612043580, 1611957180]

    def testGetGeolocation(self):
        # Test 1 correct city name
        geolocation = self.weatherApp.getGeoLocation("Braslaw")
        assert geolocation.address == 'Браслав, Браславский район, Витебская область, Беларусь'
        assert geolocation.latitude == 55.639469
        assert geolocation.longitude == 27.031643

        # Test 2 incorrect city name
        geolocation = self.weatherApp.getGeoLocation("ggggggggggggggg")
        # if city name will be incorrect it will return None, and after that in routes it will redirect to notFound
        assert geolocation is None
