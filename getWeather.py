from datetime import datetime
from typing import Dict, List

import requests
from geopy import Nominatim, Location
from requests import Response

from constants import (
    getWeatherEndpoint,
    GetWeatherApiMethods,
    APP_ID,
    DEFAULT_EXCLUDE,
    DEFAULT_CITY,
    DAY_SECONDS,
    ABSOLUT_ZERO,
)
from models import DailyWeatherResponse, WeatherInfo, PastDailyWeatherInfo


class GetWeather:
    def __init__(self):
        self.endpoint: str = getWeatherEndpoint

    def callWeatherApi(self, method: str, params: Dict) -> Dict:
        """
        Performs a request to the weather api.
        :method: str :
        :params: Dict: params for api call
        :return: Dict: json response
        """
        url: str = f"{self.endpoint}{method}"
        response: Response = requests.get(url, params=params)
        if not response.ok:
            raise Exception(f"Text: {response.text}. Status code: {response.status_code}")
        responseJson: Dict = response.json()
        return responseJson

    def getCurrentWeather(self, latitude: float, longitude: float) -> WeatherInfo:
        """
        Returns current weather info
        :latitude: float : lat coordinate
        :longitude: float: lon coordinate
        :return: WeatherInfo: object of weather info
        """
        params: Dict = {"lat": latitude, "lon": longitude, "appid": APP_ID}
        response: Dict = self.callWeatherApi(GetWeatherApiMethods.current, params)
        weatherInfo: WeatherInfo = WeatherInfo(response)
        return weatherInfo

    def getDailyWeather(
        self, latitude: float, longitude: float, exclude: str = DEFAULT_EXCLUDE
    ) -> DailyWeatherResponse:
        """
        Returns daily weather info
        :latitude: float : lat coordinate
        :longitude: float: lon coordinate
        :exclude: str: param which show what will be excluded from the request
        :return: DailyWeatherResponse: object of daily weather response
        """
        params: Dict = {
            "lat": latitude,
            "lon": longitude,
            "exclude": exclude,
            "appid": APP_ID,
        }
        response: Dict = self.callWeatherApi(
            GetWeatherApiMethods.oneCall, params=params
        )
        dailyWeather: DailyWeatherResponse = DailyWeatherResponse(response)
        return dailyWeather

    def getWeatherFromPast(
        self, latitude: float, longitude: float, requestedDays: int = 5
    ) -> List[PastDailyWeatherInfo]:
        """
        Returns daily weather info from past
        :latitude: float : lat coordinate
        :longitude: float: lon coordinate
        :requestedDays: int: for how many days were the request
        :return: List[PastDailyWeatherInfo]: list of weather info for past days
        """
        params: Dict = {"lat": latitude, "lon": longitude, "appid": APP_ID}
        dtList: List[int] = self.getListOfDateTimesForPastFiveDays()
        interval: int = 0
        responseWeather: List[PastDailyWeatherInfo] = []
        for dt in dtList:
            interval += 1
            if interval > requestedDays:
                break
            params["dt"] = dt
            response: Dict = self.callWeatherApi(
                GetWeatherApiMethods.oneCallPast, params=params
            )
            todayWeatherInfo: PastDailyWeatherInfo = PastDailyWeatherInfo(
                response.get("current")
            )
            responseWeather.append(todayWeatherInfo)
        return responseWeather

    def getGeoLocation(self, cityName: str = DEFAULT_CITY) -> Location:
        """
        Returns geolocation of the city
        :cityName: str : name of the city which geolocation should be founded
        :return: Location: geolocation data
        """
        geolocator: Nominatim = Nominatim(user_agent="Your_Name")
        geolocation: Location = geolocator.geocode(cityName)
        return geolocation

    def tempToCelsius(self, tempKelvin: float) -> float:
        """
        Returns temperature in celsius
        :tempKelvin: float : temperature in kelvin
        :return: float: celsius temperature
        """
        return round(tempKelvin - ABSOLUT_ZERO, 2)

    def getListOfDateTimesForPastFiveDays(self) -> List[int]:
        """
        Used weather api takes 'dt' parameter for calls to get weather from past, 'dt' - is datetime in seconds.
        Used weather api allows to get info maximum about 5 days from past from current time. So this method returns a
        list of seconds for 5 days from the past since now
        :return: List[int]: list of seconds
        """
        now: float = datetime.now().timestamp()
        dtBeforeYstd = int(now - DAY_SECONDS)
        dtBeforeYstd2 = int(now - DAY_SECONDS * 2)
        dtBeforeYstd3 = int(now - DAY_SECONDS * 3)
        dtBeforeYstd4 = int(now - DAY_SECONDS * 4)
        dtBeforeYstd5 = int(now - DAY_SECONDS * 5)
        dtList: List = [
            dtBeforeYstd,
            dtBeforeYstd2,
            dtBeforeYstd3,
            dtBeforeYstd4,
            dtBeforeYstd5,
        ]
        return dtList
