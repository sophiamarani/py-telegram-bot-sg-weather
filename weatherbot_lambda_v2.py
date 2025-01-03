import os
import json
from datetime import datetime, timedelta
import requests
import logging
from errors import DataError, NoDataFoundError, BadRequestError, TelegramBotApiError
from telegrambot import TelegramBot
from utility import convert_iso_to_readable_date, bold_text

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level to INFO

def lambda_handler(event, context):
    
    BOT_TOKEN = os.environ.get('TOKEN')
    BASE_URL = os.environ.get('BASE_URL')

    BOT_REPLY_API_EMPTY = os.environ.get('BOT_REPLY_API_EMPTY')
    BOT_REPLY_INPUT_INVALID = os.environ.get('BOT_REPLY_INPUT_INVALID')

    def greeting():
        try:
            # Extract user details and message date
            user_first_name = message['chat']['first_name'] #bot greets user using their telegram app's first_name
            date_message = message['date'] #class: integer 
        
            # Convert the message timestamp to Singapore time (GMT+8)
            datetime_user = datetime.fromtimestamp(date_message) + timedelta(hours=8) #class: datetime.datetime
        
            # Extract the hour from the datetime
            hour_message = datetime_user.hour

            # Determine the greeting based on the time of day
            if hour_message > 20: # 21-23
                greeting = "\u522b\u6253\u6270\u6211\u7684\u7f8e\u5bb9\u89c9" #别打扰我的美容觉
            elif hour_message > 17: # 18-20
                greeting = "\u665A\u4e0a\u597d" #晚上好
            elif hour_message > 11: # 12-17
                greeting = "\u5348\u5b89" #午安
            elif hour_message > 5: # 6-11
                greeting = "\u65e9\u5b89" #早安
            else: # 0-5
                greeting = "\u4f60\u5e94\u8be5\u5c31\u5bdd\u54e6" #你应该就寝哦

            # Construct the bot's reply
            bot_reply = f"{greeting} {user_first_name}! I am your handy weather predictor. {u'\U0001F61A'}"
        
            # Send the greeting message
            bot.send_message(message['chat']['id'], message['message_id'], bot_reply)

        except KeyError as key_err:
            error_msg = f"Missing key in message data: {key_err}"
            bot.send_message(message['chat']['id'], message['message_id'], text=BOT_REPLY_API_EMPTY)
            raise TelegramBotApiError(f"Error in greeting function: {error_msg}")
        except Exception as err:
            bot.send_message(message['chat']['id'], message['message_id'], text=BOT_REPLY_API_EMPTY)
            raise TelegramBotApiError(f"Error in greeting function: {err}")

    def fetch_weather_forecast(base_url, date, endpoint):
        """
        Fetches weather forecast data from the specified API endpoint.

        Args:
            base_url (str): The base URL of the API.
            date (str): The date filter in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:mm:ss' format.
            endpoint (str): The API endpoint (e.g., 'twenty-four-hr-forecast' or 'four-day-outlook').

        Returns:
            dict: Parsed JSON response containing weather forecast data.

        Raises:
            ValueError: If the API returns a 400 error (Invalid HTTP request body).
            NoDataFoundError: If the API returns a 404 error (Weather data not found).
            BadRequestError: For other unexpected errors.
        """
        if not date:
            raise ValueError("The 'date' parameter is required and cannot be None or empty.")

        try:
            # Build the query parameters
            params = {'date': date}

            # Log the request details
            logger.info(f"Making GET request to {base_url}/{endpoint} with parameters: {params}")

            # Make the GET request
            response = requests.get(f"{base_url}/{endpoint}", params=params)

            # Raise HTTPError for bad responses
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Check for API-specific errors
            if data.get('code') != 0:
                raise BadRequestError(data.get('errorMsg', 'Unknown error'))
            
            logger.info(f"GET request to {base_url}/{endpoint}: success")
            
            return data

        except requests.exceptions.HTTPError as http_err:
            error_msg = response.json().get('errorMsg', 'Unknown error')
            if response.status_code == 400:
                raise ValueError(f"Error 400 occurred in {endpoint} API: {error_msg}")
            elif response.status_code == 404:
                raise NoDataFoundError(f"Error 404 occurred in {endpoint} API: {error_msg}")
            else:
                raise BadRequestError(f"HTTP error occurred in {endpoint} API: {http_err}")

        except requests.exceptions.RequestException as req_err:
            raise BadRequestError(f"Request error occurred in {endpoint} API: {req_err}")

        except Exception as err:
            raise BadRequestError(f"An unexpected error occurred in {endpoint} API: {err}")

    def fetch_one_day_forecast(base_url, date):
        """
        Fetches the 24-hour weather forecast from the 24-hour Weather Forecast API.

        Args:
            base_url (str): The base URL of the API.
            date (str): The date filter in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:mm:ss' format.

        Returns:
            dict: Parsed JSON response containing weather forecast data.
        """
        return fetch_weather_forecast(base_url, date, "twenty-four-hr-forecast")

    def process_one_day_forecast(data):
        """
        Extracts the latest forecast details from the API response.

        Args:
            data (dict): JSON response from the API.

        Returns:
            dict: Extracted forecast details (date, forecast text, temperature range, humidity range, wind speed and direction).
        """
        try:
            data_records = data['data']['records']
            if not data_records: # records is empty list
                return None  # No data found

            # Access the first record (assuming it is latest)
            forecast = data_records[0]
            
            # Extract required details
            general = forecast.get("general", {})
            forecast_text = general.get("forecast", {}).get("text", "N/A")
            temperature = general.get("temperature", {})
            humidity = general.get("relativeHumidity", {})
            wind = general.get("wind", {})

            # Format the output
            latest_forecast = {
                "date": convert_iso_to_readable_date(forecast.get("timestamp")),
                "forecast": forecast_text,
                "temp_range": f"{temperature.get('low', 'N/A')} \\- {temperature.get('high', 'N/A')} \u2103",
                "humid_range": f"{humidity.get('low', 'N/A')} \\- {humidity.get('high', 'N/A')} \u0025",
                "wind_range": f"{wind.get('speed', {}).get('low', 'N/A')} \\- {wind.get('speed', {}).get('high', 'N/A')} km/h",
                "wind_direction": wind.get('direction', 'N/A')
            }

            return latest_forecast

        except KeyError as err:
            raise DataError(f"Missing expected key in response data for 24-hour Weather Forecast API: {err}")
        except TypeError as err:
            raise DataError(f"Type error while processing data for 24-hour Weather Forecast API: {err}")
        except Exception as err:
            raise DataError(f"An unexpected error occurred while processing data for 24-hour Weather Forecast API: {err}")
        
    def send_today():
        try:
            date_of_message = message['date']
            date_user = datetime.fromtimestamp(date_of_message) + timedelta(hours=8)
            date_filter = date_user.strftime('%Y-%m-%d')
            # Fetch forecast data
            data = fetch_one_day_forecast(BASE_URL, date=date_filter)
            forecast = process_one_day_forecast(data)
            if not forecast:
                bot_reply = BOT_REPLY_API_EMPTY
            else:
                bot_reply = bold_text("Start your today with a hooray\\!\n\n")
                bot_reply += (
                    f"{bold_text(forecast['date'])}\n"
                    f"\u2022 {bold_text('Forecast:')} {forecast['forecast']}\n"
                    f"\u2022 {bold_text('Temperature:')} {forecast['temp_range']}\n"
                    f"\u2022 {bold_text('Humidity:')} {forecast['humid_range']}\n"
                    f"\u2022 {bold_text('Wind:')} {forecast['wind_range']}, {forecast['wind_direction']}\n\n"
                )
            # Send message
            bot.send_message(message['chat']['id'], message['message_id'], bot_reply, parse_mode="MarkdownV2")
 
        except Exception as err:
            bot.send_message(message['chat']['id'], message['message_id'], text=BOT_REPLY_API_EMPTY)
            raise TelegramBotApiError(f"Error in today function: {err}")

    def fetch_four_day_forecast(base_url, date):
        """
        Fetches the 4-day weather forecast from the 4-day Weather Forecast API.

        Args:
            base_url (str): The base URL of the API.
            date (str): The date filter in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:mm:ss' format.

        Returns:
            dict: Parsed JSON response containing weather forecast data.
        """
        return fetch_weather_forecast(base_url, date, "four-day-outlook")

    def process_four_day_forecast(data):
        """
        Processes the forecast data for the next four days.

        Args:
            data (dict): JSON response from the API.

        Returns:
            list: List of dictionaries containing forecast details for the next four days.
        """
        try:
            result_list = []
            data_records = data.get('data', {}).get('records', [])
            if not data_records: # records is empty list
                return result_list

            forecast_list = data_records[0].get('forecasts', [])
            for forecast in forecast_list:
                result_list.append({
                    'date': convert_iso_to_readable_date(forecast['timestamp']),
                    'forecast': forecast['forecast']['text'],
                    'temp_range': f"{forecast['temperature']['low']} \\- {forecast['temperature']['high']} \u2103",
                    'humid_range': f"{forecast['relativeHumidity']['low']} \\- {forecast['relativeHumidity']['high']} \u0025",
                    'wind_range': f"{forecast['wind']['speed']['low']} \\- {forecast['wind']['speed']['high']} km/h",
                    'wind_direction': forecast['wind']['direction']
                })
            return result_list

        except KeyError as err:
            raise DataError(f"Missing expected key in response data for 4-day Weather Forecast API: {err}")
        except TypeError as err:
            raise DataError(f"Type error while processing data for 4-day Weather Forecast API: {err}")
        except Exception as err:
            raise DataError(f"An unexpected error occurred while processing data for 4-day Weather Forecast API: {err}")

    def send_future():
        try:
            date_of_message = message['date']
            date_user = datetime.fromtimestamp(date_of_message) + timedelta(hours=8)
            date_filter = date_user.strftime('%Y-%m-%d')
            # Fetch forecast data
            data = fetch_four_day_forecast(BASE_URL, date=date_filter)
            forecast_list = process_four_day_forecast(data)

            if not forecast_list:
                bot_reply = BOT_REPLY_API_EMPTY
            else:
                bot_reply = bold_text("After putting my hands together, I predict such weather\u2026\n\n")
                for forecast in forecast_list:
                    bot_reply += (
                        f"{bold_text(forecast['date'])}\n"
                        f"\u2022 {bold_text('Forecast:')} {forecast['forecast']}\n"
                        f"\u2022 {bold_text('Temperature:')} {forecast['temp_range']}\n"
                        f"\u2022 {bold_text('Humidity:')} {forecast['humid_range']}\n"
                        f"\u2022 {bold_text('Wind:')} {forecast['wind_range']}, {forecast['wind_direction']}\n\n"
                    )

            bot.send_message(message['chat']['id'], message['message_id'], bot_reply, parse_mode="MarkdownV2")
        except Exception as err:
            bot.send_message(message['chat']['id'], message['message_id'], text=BOT_REPLY_API_EMPTY)
            raise TelegramBotApiError(f"Error in future function: {err}")

    try:
        bot = TelegramBot(bot_token=BOT_TOKEN)
        message = json.loads(event['body'])['message']
        
        user_input = message['text']
        username = message['from']['username']
        input_date = (datetime.fromtimestamp(message['date']) + timedelta(hours=8)).strftime('%d %b %Y, %H:%M:%S')
        logger.info(f"User @{username} inputted '{user_input}' on {input_date}.")
        
        match user_input:
            case "/start":
                greeting()
            case "/today":
                send_today()
            case "/future":
                send_future()
            case _:
                bot.send_message(message['chat']['id'], message['message_id'], text=BOT_REPLY_INPUT_INVALID)

    except Exception as e:
        logger.error(f"Error in lambda function: {e}")
