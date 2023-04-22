def is_informational(code):
    return 100 <= code <= 199


def is_success(code):
    return 200 <= code <= 299


def is_redirect(code):
    return 300 <= code <= 399


def is_client_error(code):
    return 400 <= code <= 499


def is_server_error(code):
    return 500 <= code <= 599
