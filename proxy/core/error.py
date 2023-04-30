"""
Module Error
"""


class ErrorSetupValidate(Exception):

    def __init__(self):
        message = "Error in the validation step of an HTTP request to the Proxy."
        super(ErrorSetupValidate, self).__init__(message)


class ErrorSetupStorage(Exception):

    def __init__(self):
        message = "Error in the processing step of an HTTP request to the Proxy."
        super(ErrorSetupStorage, self).__init__(message)


class ErrorManyRequests(Exception):

    def __init__(self):
        message = "Error sending too many requests in a given amount of time."
        super(ErrorManyRequests, self).__init__(message)
