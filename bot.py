#codes from pythonanywhere

# -*- coding: UTF-8 -*-
#if not for above line, will have error (on bash in pythonanywhere) >>> SyntaxError: Non-ASCII character '\xe4' in file bot.py on line 20, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details

#note: all times and dates are adjusted to Singapore's

import telebot
import time

bot_token = 'your-bot-token' #your Telegram BOT API Token from @BotFather

bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start']) #bot answers if command is start
def send_greet(message):

    userfirstname = message.chat.first_name #bot greets user using their telegram app's first_name
    date_message = message.date #class: integer

    from datetime import datetime, timedelta
    datetime_user = datetime.fromtimestamp(date_message) + timedelta(hours=8) #class: datetime.datetime #on pythonanywhere, the retrieved date of telegram message by user is UTC which is 8 hours before the actual date (SG time)

    hour_message = int(datetime_user.strftime('%H')) #get the integer of the hour of message sent by user in 24-time format

    greeting = u"\u4f60\u5e94\u8be5\u5c31\u5bdd\u54e6 " #24-time -> 0-5 #你应该就寝哦

    if hour_message > 5:
        greeting = u"\u65e9\u5b89 " #24-time -> 6-11 #早安

        if hour_message > 11:
            greeting = u"\u5348\u5b89 " #24-time -> 12-17 #午安

            if hour_message > 17: #24-time -> 18-20
                greeting = u"\u665a\u4e0a\u597d " #晚上好

                if hour_message > 20: #24-time -> 21-23
                    greeting = u"\u522b\u6253\u6270\u6211\u7684\u7f8e\u5bb9\u89c9 " #别打扰我的美容觉

    #greeting += datetime_user.strftime('%Y-%m-%d %H:%M:%S') #SG time
    bot.reply_to(message, greeting + userfirstname + "! And I am your handy weather predictor. " + u"\U0001F61A")

def get_forecastList(date):
    url = 'https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date_time=' + date + 'T00%3A00%3A00'

    import urllib, json
    #import urllib.request #pythonanywhere does not seem to support/have this
    #response = urllib.request.urlopen(url)
    from urllib2 import urlopen
    response = urlopen(url)

    data = json.loads(response.read())

    test = data['items'][0]

    if test == {}:
        return False
    else:
        forecastList = data['items'][0]['forecasts']

        list = [
            {},
            {},
            {},
            {}
        ]

        for i in range(4):
            list[i] = {
                'date': forecastList[i]['date'],
                'forecast': forecastList[i]['forecast'],
                'tempRange': str(forecastList[i]['temperature']['low']) + ' - ' + str(forecastList[i]['temperature']['high']) + u" \u2103".encode('utf8'), #if no .encode('utf8'), will have error (on bash in pythonanywhere) >>> ERROR - TeleBot: "UnicodeEncodeError occurred, args=('ascii', u'24 - 34 \u2103', 8, 9, 'ordinal not in range(128)')
                'humidRange': str(forecastList[i]['relative_humidity']['low']) + ' - ' + str(forecastList[i]['relative_humidity']['high']) + u" \u0025".encode('utf8'),
                'windRange': str(forecastList[i]['wind']['speed']['low']) + ' - ' + str(forecastList[i]['wind']['speed']['high']) +' km/h',
                'windDirection': forecastList[i]['wind']['direction']
            }

        return list

@bot.message_handler(commands=['weather'])
def send_weather(message):

    date_message = message.date

    from datetime import datetime, timedelta
    datetime_user = datetime.fromtimestamp(date_message) + timedelta(hours=8) #on pythonanywhere, the retrieved date of telegram message by user is UTC which is 8 hours before the actual date (SG time)
    date_user_str = datetime_user.strftime('%Y-%m-%d') #string
    #actual_date_user_str = datetime.fromtimestamp(date_message).strftime('%Y-%m-%d %H:%M:%S')
    #actual_date_user_obj = datetime.strptime(actual_date_user_str, '%Y-%m-%d').date()

    actual_date_user_objraw1 = datetime.fromtimestamp(date_message) + timedelta(hours=8) #on pythonanywhere, the retrieved date of telegram message by user is UTC which is 8 hours before the actual date (SG time)
    actual_date_user_str1 = actual_date_user_objraw1.strftime('%Y-%m-%d')
    actual_date_user_obj1 = datetime.strptime(actual_date_user_str1, '%Y-%m-%d').date()

    while get_forecastList(date_user_str) == False:
        datetime_user -= timedelta(days = 1)
        date_user_str = datetime_user.strftime('%Y-%m-%d')

    forecastList = get_forecastList(date_user_str) #print(forecastList)

    final_forecastList = []

    for forecast in forecastList:
        datetime_obj = datetime.strptime(forecast['date'], '%Y-%m-%d').date()
        if actual_date_user_obj1 >= datetime_obj:
            continue
        else:
            final_forecastList.append(forecast) #print(final_forecastList)

    bot_reply = "After putting my hands together, I predict such weather:\n\n"

    for forecast in final_forecastList:
        datetime_object = datetime.strptime(forecast['date'], '%Y-%m-%d')
        date = datetime_object.strftime('%d %b %Y')

        bot_reply += 'date: {}\nforecast: {}\ntemperature: {}\nhumidity: {}\nwind: {}, {}\n\n'.format(date, forecast['forecast'], forecast['tempRange'], forecast['humidRange'], forecast['windRange'], forecast['windDirection'])

    #bot_reply += actual_date_user_str #UTC time, 8 hours before SG time
    #bot_reply += '\n' + actual_date_user_objraw1.strftime('%Y-%m-%d %H:%M:%S') #SG time
    bot.reply_to(message, bot_reply)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)