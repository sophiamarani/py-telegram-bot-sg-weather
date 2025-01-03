# PocketWeather Bot

PocketWeather Bot is a Telegram bot designed to provide accurate weather forecasts for Singapore. Whether you need the weather for today or the next few days, this bot has you covered!

## Features
- **Today's Weather:** Use the `/today` command to get the 24-hour weather forecast for Singapore.
- **4-Day Forecast:** Use the `/future` command to access the 4-day weather outlook.

## Data Source
The weather data is sourced from [Data.gov.sg](https://data.gov.sg)'s 24-hour and 4-day Weather Forecasts, managed by the National Environment Agency (NEA).

## Tech Stack
- **Programming Language:** Python
- **Hosting:** AWS Lambda (serverless computing)
- **API Management:** AWS API Gateway

## Usage
1. Open Telegram and visit the bot: [@pocketweather_bot](https://t.me/pocketweather_bot).
2. Use the `/today` command to get today's weather forecast.
3. Use the `/future` command to see the weather forecast for the next 4 days.

## Set Up
1. **Create Your `.env` File**
   - Duplicate `.env.copy` and rename it to `.env`.

2. **Configure Telegram Bot token**
   - Start a conversation with [@BotFather](https://t.me/BotFather)
   - Create a new bot with a unique username
   - Get the token and add it to the `.env` file by setting `TOKEN`

3. **Configure AWS Lambda and AWS API Gateway**
   - ...
   
## License
This project is open-source and available for use under the [MIT License](LICENSE).


---

Stay informed and plan your day with PocketWeather Bot! 🌤️