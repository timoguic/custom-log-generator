"""Custom providers for special uses"""

import random


def request():
    """Returns a string that mimics some HTTP request, with method and in/out bytes

    If the method is GET, in is much larger than out.
    Otherwise, out is much larger than in.
    """
    method = "GET"
    if random.random() > 0.8:
        method = "POST"

    in_size = int(random.gauss(35000, 10000))
    out_size = int(random.gauss(1200, 300))

    if method != "GET":
        in_size, out_size = out_size, in_size

    return f"in={in_size} out={out_size} requestMethod={method}"
