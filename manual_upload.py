import logging
import time
import requests
from typing import Union

from config import IMAGE_DIR, INPUT_IMAGE, OUTPUT_IMAGE
from convert import convert, resize
from write_to_board import copy_file, create_or_update_log
from logger_util import log_function_call

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

@log_function_call
def manual_upload(filename: str, width: int, height: int, format: str) -> None:
    """
    Manually uploads an image by resizing it to the specified dimensions,
    converting it to the desired format, and then copying it to the output 
    location. It also logs the upload activity.

    Args:
        filename (str): The path of the image file to be uploaded.
        width (int): The desired width for the resized image.
        height (int): The desired height for the resized image.
        format (str): The format to which the image should be converted.

    Returns:
        None
    """
    logger.debug(f'Starting manual upload for file: {filename} with size ({width}x{height}) and format: {format}')
    resized_file: str = resize(filename, width, height)
    logger.debug(f'Resized file created: {resized_file}')

    converted_file: str = convert(resized_file, format)
    logger.debug(f'Converted file created: {converted_file}')

    copy_file(f'{IMAGE_DIR}/{converted_file}', OUTPUT_IMAGE)
    logger.debug(f'Copied file to output location: {OUTPUT_IMAGE}')

    create_or_update_log(filename)
    logger.info(f'Successfully logged upload for file: {filename}')

manual_upload(INPUT_IMAGE, 64, 64, 'bmp')