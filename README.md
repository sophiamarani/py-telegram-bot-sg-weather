# py-telegram-bot-sg-weather

(Last Updated: 6 December 2020)

Using Python to create a Telegram bot that informs the user of weather forecast(s) in Singapore. You can try my Telegram bot @pocketweather_bot.

Where do I host my Python codes? https://www.pythonanywhere.com/ 
1) Create a free account.
2) Upload your Python codes as a File.
3) Create a Bash Console.
4) Wait for Bash Console to load. Then, type "python your_python_file_name.py" and run.

Resource: https://www.youtube.com/watch?v=jhFsFZXZbu4&t=1s

Weather forecasts are sourced from 4-day Weather Forecast on Data.gov.sg website and managed by National Environment Agency. This is also the second API used (the first one is Telegram Bot API).
(https://data.gov.sg/dataset/weather-forecast?resource_id=4df6d890-f23e-47f0-add1-fd6d580447d1)

There is only 1 command:
- /weather - Tickle me and I shall share my thoughts.

Other notable resources:
- National Environment Agency's Weather (to understand the information): https://www.nea.gov.sg/weather
- URL, second API:
  - urllib.request.urlopen(url) >>> Open the URL url, which can be either a string or a Request object: https://docs.python.org/3/library/urllib.request.html
  - json.loads(response.read()) >>> Deserialize a .read(), which is a supporting text file/binary file containing a JSON document, to a Python object: https://docs.python.org/3/library/json.html
- datetime:
  - Convert Unix Timestamp to datetime, and vice versa: https://www.programiz.com/python-programming/datetime/timestamp-datetime
  - Python's strftime (to know the code(s) needed to print the string): https://strftime.org/
  - To add time to a date (datetime and timedelta): https://docs.python.org/3/library/datetime.html#timedelta-objects
- from Chinese characters to Unicode: https://www.chineseconverter.com/en/convert/unicode
