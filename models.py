from typing import Dict, List


class WeatherInfo:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.id: int = objectDict.get("id")
            self.name: str = objectDict.get("name", "")
            self.weather: List[Weather] = objectDict.get("weather", [])
            self.main: Main = Main(objectDict.get("main", {}))
            self.sys: Sys = Sys(objectDict.get("sys", {}))


class Weather:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.id: int = objectDict.get("id")
            self.main: str = objectDict.get("main", "")
            self.description: str = objectDict.get("description", "")


class Main:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.temp: float = objectDict.get("temp", 0)
            self.temp_min: float = objectDict.get("temp_min", 0)
            self.temp_max: float = objectDict.get("temp_max", 0)
            self.pressure: int = objectDict.get("pressure", 0)
            self.humidity: int = objectDict.get("humidity", 0)


class Sys:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:
            # TODO cleanup default values
            self.id: int = objectDict.get("id")
            self.country: str = objectDict.get("country", "")


class DailyTemperature:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:
            self.day: float = objectDict.get("day", 0)
            self.min: float = objectDict.get("min", 0)
            self.max: float = objectDict.get("max", 0)
            self.night: float = objectDict.get("night", 0)
            self.eve: float = objectDict.get("eve", 0)
            self.morn: float = objectDict.get("morn", 0)


class DailyWeatherInfo:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.dt: int = objectDict.get("dt", 0)
            self.temp: DailyTemperature = DailyTemperature(objectDict.get("temp"))
            self.pressure: int = objectDict.get("pressure", 0)
            self.humidity: int = objectDict.get("humidity", 0)


class DailyWeatherResponse:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.lat: int = objectDict.get("lat", 0)
            self.lon: int = objectDict.get("lon", 0)
            self.daily: List[DailyWeatherInfo] = [DailyWeatherInfo(day) for day in objectDict.get("daily")]


class PastDailyWeatherInfo:
    def __init__(self, objectDict: Dict = None):

        if objectDict is None:
            objectDict = {}

        if objectDict:

            self.dt: int = objectDict.get("dt", 0)
            self.temp: int = objectDict.get("temp", 0)
            self.pressure: int = objectDict.get("pressure", 0)
            self.humidity: int = objectDict.get("humidity", 0)
