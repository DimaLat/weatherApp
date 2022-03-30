getWeatherEndpoint: str = "http://api.openweathermap.org/data/2.5/"

ABSOLUT_ZERO: float = 273.15
DEFAULT_EXCLUDE: str = "current,hourly,minutely"
APP_ID: str = "76b4d5dba2a643e21a2d0570e8200b0a"
DEFAULT_CITY: str = "Minsk"
DAY_SECONDS: int = 86400


class GetWeatherApiMethods:
    current = "weather"
    oneCallPast = "onecall/timemachine"
    dailySixteenDays = "forecast/daily"
    oneCall = "onecall"
