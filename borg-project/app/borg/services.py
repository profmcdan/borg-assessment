import string
import random


def generate_short_url(original_url: str):
    base_url = "https://borgurl.com/"

    # Generate a random string.
    random_string = "".join(random.choice(string.ascii_lowercase) for _ in range(6))

    # Return the shortened URL.
    return {
        "short_url": f"{base_url}{random_string}",
        "code": random_string
    }


def clean_url(url: str):
    clean = url.strip().lower()
    if clean.endswith("/"):
        clean = clean[:-1]
    return clean


def get_original_url(short_url: str):
    pass


def redirect_url(short_url: str):
    pass
