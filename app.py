import os
from datetime import datetime
from typing import List, Dict

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from geopy import Location

from constants import DEFAULT_CITY
from getWeather import GetWeather
from models import WeatherInfo

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS", False
)
app.secret_key = os.getenv("SECRET_KEY", "")
weatherApp = GetWeather()

db = SQLAlchemy(app)


class WeatherToDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(80), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    averageDaytimeTemperature = db.Column(db.Numeric, nullable=False)
    averagePressure = db.Column(db.Numeric, nullable=False)
    averageHumidity = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        region,
        startDate,
        endDate,
        averageDaytimeTemperature,
        averagePressure,
        averageHumidity,
    ):
        self.region = region
        self.startDate = startDate
        self.endDate = endDate
        self.averageDaytimeTemperature = averageDaytimeTemperature
        self.averagePressure = averagePressure
        self.averageHumidity = averageHumidity


@app.route("/", methods=["GET"])
def mainPage():
    return render_template("mainPage.html")


@app.route("/saveWeatherDataToDB", methods=["POST"])
def saveWeatherDataToDB():
    if request.method == "POST":
        result = request.form
        weatherToDB = WeatherToDb(
            region=result.get("region", ""),
            startDate=result.get("startDate"),
            endDate=result.get("endDate"),
            averageDaytimeTemperature=result.get("averageTemperature", 0),
            averagePressure=result.get("averagePressure", 0),
            averageHumidity=result.get("averageHumidity", 0),
        )
        db.session.add(weatherToDB)
        db.session.commit()
    return render_template("dataSaved.html")


@app.route("/todayWeather", methods=["POST", "GET"])
def todayWeather():
    cityName: str = DEFAULT_CITY
    if request.method == "POST":
        result = request.form
        cityName = result.get("Name", "")

    geoLocation: Location = weatherApp.getGeoLocation(cityName=cityName)
    if not geoLocation:
        return render_template("notFound.html")
    try:
        weatherInfo: WeatherInfo = weatherApp.getCurrentWeather(
            latitude=geoLocation.latitude,
            longitude=geoLocation.longitude,
        )
    except Exception as exc:
        return render_template("notFound.html", excText=exc)
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
    try:
        weather = weatherApp.getDailyWeather(
            latitude=geoLocation.latitude, longitude=geoLocation.longitude
        )
    except Exception as exc:
        return render_template("notFound.html", excText=exc)
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
        "region": geoLocation.address,
        "startDate": datetime.fromisoformat(
            weatherByDayList[0].get("dayDate")
        ),  # first day date
        "endDate": datetime.fromisoformat(
            weatherByDayList[-1].get("dayDate")
        ),  # last day date
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
    try:
        weatherByDays = weatherApp.getWeatherFromPast(
            latitude=geoLocation.latitude,
            longitude=geoLocation.longitude,
            requestedDays=daysInterval,
        )
    except Exception as exc:
        return render_template("notFound.html", excText=exc)
    resultAvgTemp: float = 0  # average temperature of all selected days
    resultAvgPressure: float = 0  # average pressure of all selected days
    resultAvgHumidity: int = 0  # average humidity of all selected days
    weatherByDayList: List = []
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
        "region": geoLocation.address,
        "startDate": datetime.fromtimestamp(weatherByDays[0].dt),  # first day date
        "endDate": datetime.fromtimestamp(weatherByDays[-1].dt),  # last day date
    }
    return render_template(
        "dailyWeatherForecast.html",
        avgData=avgData,
        weatherByDayList=weatherByDayList,
        geoLocation=geoLocation,
    )


if __name__ == "__main__":
    db.create_all()
    app.run()
