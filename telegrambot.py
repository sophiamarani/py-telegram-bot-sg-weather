import requests
import json
from v2.errors import TelegramBotApiError

class TelegramBot:
    def __init__(self, bot_token: str):
        self.__bot_token = bot_token  # Private field for the bot token

    def get_bot_token(self):
        """Method to safely access the bot token."""
        return self.__bot_token

    def set_bot_token(self, new_token: str):
        """Method to safely update the bot token."""
        if not new_token:
            raise ValueError("Bot token cannot be empty.")
        self.__bot_token = new_token

    def send_message(self, chat_id: str, message_id: int, text: str, parse_mode: str = None):
        """
        Sends a message to a Telegram chat.

        :param chat_id: ID of the chat (Integer or String)
        :param message_id: ID of the message to reply to
        :param text: Text message to be sent
        :param parse_mode: (Optional) Formatting style for the message
        :return: Response object from the API call
        """
        reply_parameters = {"message_id": message_id}
        send_text = (
            f'https://api.telegram.org/bot{self.__bot_token}/sendMessage?chat_id={chat_id}'
            f'&reply_parameters={json.dumps(reply_parameters)}'
            f'&text={text}'
        )

        # Include parse_mode if provided
        if parse_mode:
            send_text += f"&parse_mode={parse_mode}"

        response = requests.get(send_text)

        if response.status_code != 200:
            err = response.json()
            raise TelegramBotApiError(f"Error in sendMessage: {err}")

        return response
