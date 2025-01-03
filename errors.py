class DataError(Exception):
    """Exception raised when there is data processing error"""
    def __init__(self, message="Data processing error"):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

class NoDataFoundError(Exception):
    """Exception raised when no data is found for the given search criteria."""
    def __init__(self, message="No data found"):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"    

class BadRequestError(Exception):
    """Exception raised when the HTTP request body is invalid."""
    def __init__(self, message="Invalid HTTP request body"):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

class TelegramBotApiError(Exception):
    """Exception raised when the Telegram Bot API is invalid."""
    def __init__(self, message="Invalid Telegram Bot API"):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
