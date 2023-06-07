import re

def is_valid_url(url):
  """
  Validates if a given input is a valid URL.

  Args:
    url: The URL to validate.

  Returns:
    True if the URL is valid, False otherwise.
  """

  # Check if the URL is a valid HTTP or HTTPS URL.
  if not re.match(r'^https?://', url):
    return False

  # Check if the URL contains a valid domain name.
  if not re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]+$', url.split('/')[2]):
    return False

  # Check if the URL contains a valid port number.
  if re.match(r':(\d+)', url):
    if int(re.match(r':(\d+)', url).group(1)) < 1 or int(re.match(r':(\d+)', url).group(1)) > 65535:
      return False

  return True