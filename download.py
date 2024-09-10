import requests
import logging
import urllib.request
import json
from typing import Optional, Tuple

from config import TIMEOUT_S, LASTFM_URL, LASTFM_PUBLIC_API_KEY
from logger_util import log_function_call

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

@log_function_call
def fetch_last_played(session: requests.Session, api_key: str, user: str) -> Optional[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]:
    url = f'{LASTFM_URL}&user={user}&api_key={LASTFM_PUBLIC_API_KEY}&format=json'
    logger.info("Fetching last played track info from Last.fm API.")
    logger.debug(f"Constructed URL: {url}")
    try:
        response = session.get(url, timeout=TIMEOUT_S)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info("Successfully fetched data from Last.fm API.")

        obj = response.json()
        recent_tracks = obj.get('recenttracks', {}).get('track', [])

        if recent_tracks:
            track_info = recent_tracks[0]
            lastplayed_trackname = track_info.get('name')
            lastplayed_artist = track_info.get('artist', {}).get('#text')
            lastplayed_album = track_info.get('album', {}).get('#text')
            lastplayed_image_url = track_info.get('image', [None, None, None, None])[3]['#text']

            logger.debug("Last played track details retrieved successfully.")
            logger.info(f"Track: {lastplayed_trackname}, Artist: {lastplayed_artist}, Album: {lastplayed_album}, Image URL: {lastplayed_image_url}")
            return lastplayed_trackname, lastplayed_artist, lastplayed_album, lastplayed_image_url
        logger.warning("No recent tracks found for the user.")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

    return None, None, None, None


@log_function_call
def download_cover(session: requests.Session, image_url: str, filename: str) -> Optional[str]:
    logger.info(f"Attempting to download image from: {image_url}")
    response = session.get(image_url, timeout=TIMEOUT_S)
    if response.status_code == 200:
        logger.debug(f"Image downloaded successfully from {image_url}. Saving to ./images/{filename}")
        with open(f"./images/{filename}", 'wb') as file:
            file.write(response.content)
        logger.info(f"Image saved successfully as: {filename}")
        return filename
    else:
        logger.error(f"Failed to download image from {image_url}, status code: {response.status_code}")
        return None
