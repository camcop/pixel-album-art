import os
import logging
from typing import Optional, Callable, Any
from functools import wraps

from PIL import Image

from config import IMAGE_DIR, SUPPORTED_EXTS
from logger_util import log_function_call

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

@log_function_call
def convert(filename: str, output_ext: str) -> Optional[str]:
    file_name, input_ext = os.path.splitext(filename)

    input_ext = input_ext.lstrip('.')
    if input_ext == output_ext:
        logger.info(f'No conversion needed for {filename}')
        return filename
    if input_ext not in SUPPORTED_EXTS or output_ext not in SUPPORTED_EXTS:
        logger.error(f'Unsupported file type: {input_ext if input_ext not in SUPPORTED_EXTS else output_ext}')
        return None
    try:
        logger.info(f'Opening {filename}')
        image = Image.open(os.path.join(IMAGE_DIR, filename))
        output_filename = f'{file_name}.{output_ext}'
        logger.info(f'Saving {output_filename}')
        image.save(os.path.join(IMAGE_DIR, output_filename), output_ext)
        logger.info(f'Successfully converted {filename} to {output_filename}')
        return output_filename
    except FileNotFoundError:
        logger.error(f'Could not find {filename} in {IMAGE_DIR}')
    except Exception as e:
        logger.error(f'Error processing image file {filename}: {e}')


@log_function_call
def resize(filename: str, width: int, height: int) -> Optional[str]:
    try:
        logger.info(f'Opening image file: {filename}')
        image = Image.open(os.path.join(IMAGE_DIR, filename))

        # Resize the image.
        logger.info(f'Resizing the image to width: {width}, height: {height}')
        image = image.resize((width, height)).convert('RGB')

        directory = os.path.dirname(os.path.join(IMAGE_DIR, filename))
        file_name, file_extension = os.path.splitext(filename)

        # Change .jpg to .jpeg if necessary.
        if file_extension == '.jpg':
            file_extension = '.jpeg'
            logger.info(f'Outputting .jpg as .jpeg for compatibility with convert method')

        resized_filename = f'{file_name}{width}x{height}{file_extension}'
        resized_filepath = os.path.join(directory, resized_filename)

        logger.info(f'Saving resized image to: {resized_filepath}')
        image.save(resized_filepath)
        logger.info(f'Successfully resized and saved image: {resized_filepath}')
        return resized_filename
    except FileNotFoundError:
        logger.error(f'Could not find image file: {filename} in {IMAGE_DIR}')
    except Exception as e:
        logger.error(f'Error processing image file: {filename}. Error: {e}')

