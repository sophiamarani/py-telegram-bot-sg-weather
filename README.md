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
   - Start a conversation with [@BotFather](https://t.me/BotFather).
   - Create a new bot with a unique username.
   - Get the token and add it to the `.env` file by setting `TOKEN`.

## Configure AWS Lambda and AWS API Gateway

#### Add Code to Lambda
Upload your Python code to an AWS Lambda function.

#### Adding Environment Variables
1. Go to **Lambda > Functions > your_function**.
2. Scroll down to the **Configuration** tab.
3. Click on **Environment variables**.
4. Add the environment variables from your `.env` file.

#### Adding Lambda Layers
1. Go to **Lambda > Functions > your_function**.
2. Scroll down to the **Layers** section.
3. Click **Add a layer** and configure:
   - **Layer source:** AWS layers
     - Select **AWS-AppConfig-Extension** and choose the latest version.
   - **Layer source:** AWS layers
     - Select **AWSOpenTelemetryDistroPython** and choose the latest version.

#### Configuring Runtime Settings
Edit the **Handler** field based on your Python file name and function name.  
For example: If your file is `weatherbot_lambda_v2.py` and the function is `lambda_handler`, set the handler to `weatherbot_lambda_v2.lambda_handler`.

#### Configuring API Gateway
1. Go to **API Gateway > APIs > Create API**.
2. Choose an API type:
   - Select **HTTP API**.
3. Configure Integrations:
   - Select **Lambda** and pick your Lambda function from the dropdown list.
4. Configure Routes:
   - **Method:** ANY  
   - **Resource path:** `/`
5. After successful creation, the API Gateway will be linked to your Lambda function.

#### Add API Gateway (Webhook Link) to Telegram
1. Go to **API Gateway > APIs > your_api_gateway**.
2. Copy the **Default endpoint** value.
3. Run the following URL in your browser or a tool like Postman:
https://api.telegram.org/bot{your_bot_token}/setWebhook?url={default_endpoint_value}

## Resources
**Telegram Bot API Documentation (Official)**  
- [Available Methods](https://core.telegram.org/bots/api#available-methods)  
  - This bot uses the `sendMessage` method.  
- [Available Types (Objects)](https://core.telegram.org/bots/api#available-types)  

## License
This project is open-source and available for use under the [MIT License](LICENSE).


---

Stay informed and plan your day with PocketWeather Bot! 🌤️
