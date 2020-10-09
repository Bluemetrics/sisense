class RequestError(Exception):

    def __init__(self, message: str, code: int):
        super(RequestError, self).__init__(message)
        self.code = code
