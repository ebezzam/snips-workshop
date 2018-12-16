from __future__ import print_function
import pyowm
from api_keys import owm_key  # set `owm_key` to key from `https://home.openweathermap.org/api_keys`


city = "Lausanne"

# connect to web API
owm = pyowm.OWM(owm_key)
observation = owm.weather_at_place(city)
w = observation.get_weather()

# Weather details
print("Temperature", end=": ")
print(w.get_temperature('celsius'))
print("Cloudy", end=": ")
print(w.get_clouds())
print("Rain", end=": ")
print(w.get_rain())
print("Snow", end=": ")
print(w.get_snow())
print("Sunrise", end=": ")
print(w.get_sunrise_time('iso'))
print("Sunset", end=": ")
print(w.get_sunset_time('iso'))
print("Wind", end=": ")
print(w.get_wind())
print("Humidity", end=": ")
print(w.get_humidity())

