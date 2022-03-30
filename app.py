from datetime import datetime
from typing import List, Dict

from flask import Flask, render_template, request
from geopy import Location

from constants import DEFAULT_CITY
from getWeather import GetWeather
from models import WeatherInfo

app = Flask(__name__)
weatherApp = GetWeather()


@app.route("/")
def mainPage():
    return render_template("mainPage.html")


@app.route("/todayWeather", methods=["POST", "GET"])
def todayWeather():
    cityName: str = DEFAULT_CITY
    if request.method == "POST":
        result = request.form
        cityName = result.get("Name")

    geoLocation: Location = weatherApp.getGeoLocation(cityName=cityName)
    if not geoLocation:
        return render_template("notFound.html")
    weatherInfo: WeatherInfo = weatherApp.getCurrentWeather(
        latitude=geoLocation.latitude,
        longitude=geoLocation.longitude,
    )
    tempCelsius: float = weatherApp.tempToCelsius(weatherInfo.main.temp)
    weather_info: Dict = {
        "temperature": tempCelsius,
        "humidity": weatherInfo.main.humidity,
        "pressure": weatherInfo.main.pressure,
    }
    return render_template(
        "currentWeather.html",
        geoLocation=geoLocation,
        weather_info=weather_info,
    )


@app.route("/dailyWeatherForecast", methods=["POST", "GET"])
def dailyWeatherForecast():
    cityName: str = DEFAULT_CITY
    daysInterval: int = 7  # default 7
    if request.method == "POST":
        result = request.form
        cityName = result.get("Name")
        daysInterval = int(result.get("Days"))

    geoLocation: Location = weatherApp.getGeoLocation(cityName=cityName)
    if not geoLocation:
        return render_template("notFound.html")
    weather = weatherApp.getDailyWeather(
        latitude=geoLocation.latitude, longitude=geoLocation.longitude
    )
    weatherByDayList: List = []
    interval: int = 0
    resultAvgTemp: float = 0  # average temperature of all selected days
    resultAvgPressure: float = 0  # average pressure of all selected days
    resultAvgHumidity: int = 0  # average humidity of all selected days
    for day in weather.daily:
        interval += 1
        if interval > daysInterval:
            break
        dayDate = datetime.fromtimestamp(day.dt)
        averageHumidity = day.humidity
        averagePressure = day.pressure
        averageTemp: float = (
            day.temp.day
            + day.temp.max
            + day.temp.min
            + day.temp.morn
            + day.temp.eve
            + day.temp.night
        ) / 6
        resultAvgTemp += averageTemp
        resultAvgPressure += averagePressure
        resultAvgHumidity += averageHumidity
        weatherByDay: Dict = {
            "dayDate": str(dayDate.date()),
            "averageHumidity": averageHumidity,
            "averagePressure": averagePressure,
            "averageTemp": weatherApp.tempToCelsius(averageTemp),
        }
        weatherByDayList.append(weatherByDay)
    avgData: Dict = {
        "resultAvgTemp": weatherApp.tempToCelsius(resultAvgTemp / daysInterval),
        "resultAvgPressure": round(resultAvgPressure / daysInterval, 2),
        "resultAvgHumidity": int(resultAvgHumidity / daysInterval),
    }
    return render_template(
        "dailyWeatherForecast.html",
        weatherByDayList=weatherByDayList,
        geoLocation=geoLocation,
        avgData=avgData,
    )


@app.route("/pastWeatherForecast", methods=["POST", "GET"])
def pastWeatherForecast():
    cityName: str = DEFAULT_CITY
    daysInterval: int = 5  # default 5
    if request.method == "POST":
        result = request.form
        cityName = result.get("Name")
        daysInterval = int(result.get("Days"))
    geoLocation: Location = weatherApp.getGeoLocation(cityName=cityName)
    if not geoLocation:
        return render_template("notFound.html")
    weatherByDays = weatherApp.getWeatherFromPast(
        latitude=geoLocation.latitude,
        longitude=geoLocation.longitude,
        requestedDays=daysInterval,
    )
    resultAvgTemp: float = 0  # average temperature of all selected days
    resultAvgPressure: float = 0  # average pressure of all selected days
    resultAvgHumidity: int = 0  # average humidity of all selected days
    weatherByDayList = []
    for day in weatherByDays:
        resultAvgHumidity += day.humidity
        resultAvgPressure += day.pressure
        resultAvgTemp += day.temp
        weatherByDay: Dict = {
            "dayDate": str(datetime.fromtimestamp(day.dt).date()),
            "averageHumidity": day.humidity,
            "averagePressure": day.pressure,
            "averageTemp": weatherApp.tempToCelsius(day.temp),
        }
        weatherByDayList.append(weatherByDay)

    avgData: Dict = {
        "resultAvgTemp": weatherApp.tempToCelsius(resultAvgTemp / daysInterval),
        "resultAvgPressure": round(resultAvgPressure / daysInterval, 2),
        "resultAvgHumidity": int(resultAvgHumidity / daysInterval),
    }
    return render_template(
        "dailyWeatherForecast.html",
        avgData=avgData,
        weatherByDayList=weatherByDayList,
        geoLocation=geoLocation,
    )


if __name__ == "__main__":
    app.run()
