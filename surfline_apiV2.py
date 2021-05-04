#%%
import requests
import json 

#Function to convert a wind orientation in degrees in a cardinal direction

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return (arr[(val % 16)])

#Function to convert speed of wind from kmph in knots

def kmh_to_kn(v):
    return int(v/1.852)

#Function to convert temperature form kelvin to celsius

def kelv_to_celsius(temp):
    return (int(temp-273.15))


#Dictionnary of the spots names and their ID in the surfline API
spots_id = {
    'Blancs Sablons': '584204204e65fad6a770904c',
    'Le Petit Minou': '584204204e65fad6a7709007',
    'La Palue' : '584204204e65fad6a7709009',
    'Baie des Trepasses': '584204204e65fad6a770900e',
    'Porsmilin' : '584204204e65fad6a7709003',
    'Dalbos' : '584204204e65fad6a7709004',
    'Anse de Pen Hat' : '584204204e65fad6a7709008',
    'Kerloch': '584204204e65fad6a7709005',
    'Cap de la Chevre' : '584204204e65fad6a770900a',
    'Pointe de Dinan' : '584204204e65fad6a7709006',
    'Pors ar Vag' : '584204204e65fad6a770900c'
}



class Forecast:

    def __init__(self,spot):

        params = {
            'spotId' :'584204204e65fad6a7709007',
            'days' : '1',
            'intervalHours' : '24'
        }

        params['spotId']=spots_id[spot]
        
        self.params = params
        self.spot = spot
        self.temperature = 0
        self.temperature_feels_like = 0
        self.weather_description = ''
        self.wind_speed = 0
        self.wind_gusts = 0
        self.wind_direction = 'N'
        self.tide = 0
        self.period = 0
        self.wave_height = 0
        self.score = 0
        

    #Method wich send a string describing the waves condition on the choosen spot
    def send_wave(self):
        wave =  requests.get('https://services.surfline.com/kbyg/spots/forecasts/wave' ,params=self.params).json()

        self.wave = wave
        self.period = wave['data']['wave'][0]['swells'][0]['period']
        self.wave_height = wave['data']['wave'][0]['surf']['max']
        self.score = wave['data']['wave'][0]['surf']['optimalScore']
        
        return f"The waves at {self.spot} are {self.wave_height} m high today, with a {self.period} s period"

    #Method wich send a string describing the wind condition on the choosen spot
    def send_wind(self):

        wind =  requests.get('https://services.surfline.com/kbyg/spots/forecasts/wind', params=self.params).json()

        self.wind_speed = wind['data']['wind'][0]['speed']
        self.wind_gusts = wind['data']['wind'][0]['gust']
        self.wind_direction = degToCompass(wind['data']['wind'][0]['direction'])

        return f"the wind at {self.spot} is blowing at {int(self.wind_speed)} km/h ({kmh_to_kn(self.wind_speed)} knots), gusting at {int(self.wind_gusts)} km/h ({kmh_to_kn(self.wind_gusts)} knots), coming from {self.wind_direction}"

    #Method wich send a string describing the waves condition on the choosen spot
    def send_weather(self):

        weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=48.4&lon=-4.5&appid=8d088d57db40bc0e85ee66ddaf48f9db").json()

        weather_description = weather['weather'][0]['description']
        air_temperature = weather['main']['temp']
        air_temperature_feels_like = weather['main']['feels_like']

        self.weather_description = weather_description
        self.temperature = kelv_to_celsius(air_temperature)
        self.temperature_feels_like = kelv_to_celsius(air_temperature_feels_like)
        

        return f"the temperature of the air at {self.spot} is {self.temperature} °C, it feels like {self.temperature_feels_like} °C, the sky is {self.weather_description}"

    def send_period(self):

        wave =  requests.get('https://services.surfline.com/kbyg/spots/forecasts/wave' ,params=self.params).json()

        self.wave = wave
        self.period = wave['data']['wave'][0]['swells'][0]['period']

        return f"The period at {self.spot} is {self.period} s"
    
    def send_score(self):
        wave =  requests.get('https://services.surfline.com/kbyg/spots/forecasts/wave' ,params=self.params).json()

        self.wave = wave
        self.score = wave['data']['wave'][0]['surf']['optimalScore']


        if self.score == 0:
            return "The conditions are pretty bad for surfing today"
        if self.score == 1:
            return "The conditions are kinda good for surfing today"
        if self.score == 2:
            return "The conditions are siiiiick for surfing today"

    def send_tide(self):

        tide =  requests.get('https://services.surfline.com/kbyg/spots/forecasts/tides',params=self.params).json()
        self.tide = str(int((100 * (tide['data']['tides'][0]['height'] - tide['associated']['tideLocation']['min']) / (tide['associated']['tideLocation']['max']-tide['associated']['tideLocation']['min']))))+" % of high tide"


        return f"The tide is {self.tide} at {self.spot}"
        


# %%
