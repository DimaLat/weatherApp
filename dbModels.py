# from app import db
#
#
# class WeatherToDb(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     region = db.Column(db.String(80), nullable=False)
#     startDate = db.Column(db.Date, nullable=False)
#     endDate = db.Column(db.Date, nullable=False)
#     averageDaytimeTemperature = db.Column(db.DECIMAL, nullable=False)
#     averagePressure = db.Column(db.DECIMAL, nullable=False)
#     averageHumidity = db.Column(db.Integer, nullable=False)
#
#     def __init__(
#         self,
#         region,
#         startDate,
#         endDate,
#         averageDaytimeTemperature,
#         averagePressure,
#         averageHumidity,
#     ):
#         self.region = region
#         self.startDate = startDate
#         self.endDate = endDate
#         self.averageDaytimeTemperature = averageDaytimeTemperature
#         self.averagePressure = averagePressure
#         self.averageHumidity = averageHumidity
