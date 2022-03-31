This application was made for getting and saving weather forecast to the database. 
It was made by using Flask framework, ORM is SQLAlchemy and  PostgreSQL database.
Also code is using https://openweathermap.org/api weather api (unfortunately, only calls
for 5 days in the past and 7 days in the future are free, if you want more info you must
pay for the api to get unique app id to get access to paid content)

Here you can see the main page of the application. User can choose for which city
he wants to know the weather and also for which time (3 options: current city weather,
future weather for 1-7 days, or weather from the pas 1-5 days)

![img.png](img.png)

For example, if you want to know current weather, you need to fill in input field
and press submit button, the result is in the screenshot:
![img_1.png](img_1.png)

If you'll choose to know future weather, the result will be like on the screenshot.
You could also turn back to main page by pressing 'back' button. The resulting page will
contain info about city name, table with collected data, and average data for selected days period.
(Brest city and 6 days):
![img_2.png](img_2.png)

Also there is a case to save collected data to database (by pressing 'save' button), 
the result is in the next
screenshots:
![img_3.png](img_3.png)
![img_4.png](img_4.png)

If you'll choose to know weather from the past, you will see this (also could be saved to db)
![img_5.png](img_5.png)
![img_6.png](img_6.png)