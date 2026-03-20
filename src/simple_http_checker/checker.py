import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)

print(f"checker.py: {__name__}")

def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """
    Checks a list of URLs and returns their status
    :param urls: A list of URLs to check
    :param timeout: Max time in seconds to wait for each request to complete. Default 5s
    :return: Dictionary mapping each url to the request status
    """

    logger.info(f"Starting check for {len(urls)} URLs with a timeout of {timeout}")
    results = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning(f"Connection error for {url}")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"Unexpected request error occurred for {url}: {e}", exc_info=True)

        results[url] = status
        logger.debug(f"Checked: {url:<40} -> {status}") #40 char width with left hand orientation

    logger.info("URL checks completed")

    return results