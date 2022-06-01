from requests import Response


class BadRequest(Exception):

    def __init__(self, response: Response, message: str) -> None:
        self.response = response
        self.message = message
        super().__init__(message)
