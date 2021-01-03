
DISTANCE_VELIB_INT = 500
DISTANCE_WEATHER_INT = 1500

API_METRO_URL = "https://api-ratp.pierre-grimaud.fr/v4/traffic"

API_VELIB_URL = 'https://opendata.paris.fr/api/records/1.0/search/\
?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=\
is_installed&facet=is_renting&facet=is_returning&facet=\
nom_arrondissement_communes&geofilter.distance='+\
str("__LATITUDE__")+'%2C+'+str("__LONGITUDE__")+'%2C'+ str(DISTANCE_VELIB_INT)

API_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + \
str("__LATITUDE__") + '&lon=' + str("__LONGITUDE__") +\
'&exclude=minutely&units=metric&lang=en&appid=5644d731bfbad53e72bb6817c4473e23'

API_METEOFRANCE_RAIN_URL = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=arome-0025-sp1_sp2&q=&rows=500&geofilter.distance=' + str("__LATITUDE__") + '%2C+' + str("__LONGITUDE__") + '%2C' + str(DISTANCE_WEATHER_INT)

MAPPING_WEATHER_ICONS = {
    'thunderstorm with light rain':'tsra.svg',
    'thunderstorm with rain':'tsra.svg',
    'thunderstorm with heavy rain':'tsra.svg',
    'light thunderstorm':'tsra.svg',
    'thunderstorm':'tsra.svg',
    'heavy thunderstorm':'tsra.svg',
    'ragged thunderstorm':'tsra.svg',
    'thunderstorm with light drizzle':'tsra.svg',
    'thunderstorm with drizzle':'tsra.svg',
    'thunderstorm with heavy drizzle':'tsra.svg',
    'light intensity drizzle':'shra.svg',
    'drizzle':'shra.svg',
    'heavy intensity drizzle':'shra.svg',
    'light intensity drizzle rain':'shra.svg',
    'drizzle rain':'shra.svg',
    'heavy intensity drizzle rain':'shra.svg',
    'shower rain and drizzle':'shra.svg',
    'heavy shower rain and drizzle':'shra.svg',
    'shower drizzle':'shra.svg',
    'light rain':'hishwrs.svg',
    'moderate rain':'hishwrs.svg',
    'heavy intensity rain':'hishwrs.svg',
    'very heavy rain':'hishwrs.svg',
    'extreme rain':'hishwrs.svg',
    'freezing rain':'fzra.svg',
    'light intensity shower rain':'shra.svg',
    'shower rain':'shra.svg',
    'heavy intensity shower rain':'shra.svg',
    'ragged shower rain':'shra.svg',
    'rain and snow': 'rasn.svg',
    'light snow':'sn.svg',
    'Snow':'sn.svg',
    'Heavy snow':'sn.svg',
    'Sleet':'sn.svg',
    'Light shower sleet':'sn.svg',
    'Shower sleet':'sn.svg',
    'Light rain and snow':'sn.svg',
    'Rain and snow':'sn.svg',
    'Light shower snow':'sn.svg',
    'Shower snow':'sn.svg',
    'Heavy shower snow':'sn.svg',
    'mist':'mist.svg',
    'Smoke':'mist.svg',
    'Haze':'mist.svg',
    'sand/ dust whirls':'mist.svg',
    'fog':'mist.svg',
    'sand':'mist.svg',
    'dust':'mist.svg',
    'volcanic ash':'mist.svg',
    'squalls':'mist.svg',
    'tornado':'mist.svg',
    'clear sky':'sun.svg',
    'few clouds':'few.svg',
    'scattered clouds':'sct.svg',
    'broken clouds':'bkn.svg',
    'overcast clouds':'ovc.svg'
}
