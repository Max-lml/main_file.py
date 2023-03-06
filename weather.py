from config import open_weather_token
import requests
import datetime

result = []


def get_weather(city, open_weather_token):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Облачно \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U00002744',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/find?q={city}&type=like&APPID={open_weather_token}&units=metric'
        )
        data = r.json()

        weather_description = data['list'][0]['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там'
        city = data['list'][0]['name']
        cur_weather = data['list'][0]['main']['temp']
        humidity = data['list'][0]['main']['humidity']
        pressure = data['list'][0]['main']['pressure']
        wind = data['list'][0]['wind']['speed']
        result = (f'   {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}   \nГород: {city}\n'
        f'Температура: {round(cur_weather)}°C {wd}\n'
        f'Влажность: {humidity}\n'
        f'Давление: {pressure}мм рт.ст.\nСкорость ветра: {wind}м/с\n')
        return result
    except Exception as ex:
        print(ex)


def main():
    city = input('Введите город: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
