"""
Module Error
"""


class ErrorValidateProxy(Exception):

    def __init__(self):
        message = "Error in the validation step of an HTTP request to the Proxy."
        super(ErrorValidateProxy, self).__init__(message)
