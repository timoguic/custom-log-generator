import random


def request():
    method = "GET"
    if random.random() > 0.8:
        method = "POST"

    in_size = int(random.gauss(35000, 10000))
    out_size = int(random.gauss(1200, 300))

    if method != "GET":
        in_size, out_size = out_size, in_size

    return f"in={in_size} out={out_size} requestMethod={method}"
