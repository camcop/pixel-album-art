import os
import logging
from PIL import Image
from config import IMAGE_DIR, SUPPORTED_EXTS

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
from typing import Tuple, Optional

def convert(filename: str, output_ext: str) -> Optional[str]:
    """
    Convert an image file to a specified output format.

    Parameters:
    - filename (str): The name of the image file to convert.
    - output_ext (str): The desired output file extension (format).

    Returns:
    - Optional[str]: The name of the converted file if successful, otherwise None.
    
    Logs messages at various steps in the conversion process.
    """
    file_name, input_ext = os.path.splitext(filename)

    input_ext = input_ext.lstrip('.')
    if input_ext == output_ext:
        logger.info(f'No conversion needed for {filename}')
        return None
    if input_ext not in SUPPORTED_EXTS:
        logger.error(f'Unsupported file type {input_ext}')
        return None
    if output_ext not in SUPPORTED_EXTS:
        logger.error(f'Unsupported file type {output_ext}')
        return None
    logger.info(f'Converting {filename} from {input_ext} to {output_ext}')

    try:
        logger.info(f'Opening {filename}')
        image = Image.open(os.path.join(IMAGE_DIR, filename))
    except FileNotFoundError:
        logger.error(f'Could not find {filename} in {IMAGE_DIR}')
        return None
    except Exception as e:
        logger.error(f'Error opening image file {filename}: {e}')
        return None
    try:
        output_filename = f'{file_name}.{output_ext}'
        logger.info(f'Saving {output_filename}')
        image.save(os.path.join(IMAGE_DIR, output_filename), output_ext)
        logger.info(f'Successfully converted {filename} to {output_filename}')
    except Exception as e:
        logger.error(f'Could not save {output_filename}. Error: {e}')
        return None
    return output_filename


def resize(filename: str, width: int, height: int) -> Optional[str]:
    """
    Resize an image file to specified dimensions.

    Parameters:
    - filename (str): The name of the image file to resize.
    - width (int): The target width of the resized image.
    - height (int): The target height of the resized image.

    Returns:
    - Optional[str]: The name of the resized image file if successful, otherwise None.
    
    Logs messages at various steps in the resizing process.
    """
    logger.info(f'Resizing image: {filename} to width: {width}, height: {height}')
    try:
        logger.info(f'Opening image file: {filename}')
        image = Image.open(os.path.join(IMAGE_DIR, filename))
    except FileNotFoundError:
        logger.error(f'Could not find image file: {filename} in {IMAGE_DIR}')
        return None
    except Exception as e:
        logger.error(f'Error opening image file: {filename}. Error: {e}')
        return None
    logger.info(f'Resizing the image')
    image = image.resize((width, height)).convert('RGB')

    directory = os.path.dirname(os.path.join(IMAGE_DIR, filename))
    file_name, file_extension = os.path.splitext(filename)

    if file_extension == '.jpg':
        file_extension = '.jpeg'
        logger.info(f'Outputting .jpg as .jpeg for compatibility with convert method')

    resized_filename = f'{file_name}{width}x{height}{file_extension}'
    resized_filepath = os.path.join(directory, resized_filename)

    try:
        logger.info(f'Saving resized image to: {resized_filepath}')
        image.save(resized_filepath)
        logger.info(f'Successfully resized and saved image: {resized_filepath}')
    except Exception as e:
        logger.error(f'Could not save resized image to {resized_filepath}. Error: {e}')
        return None
    return resized_filename
