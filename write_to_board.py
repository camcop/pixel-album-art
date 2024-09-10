import os
import logging
import shutil

from config import BOARD_DRIVE_LETTER, LOG_FILENAME
from logger_util import log_function_call

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

@log_function_call
def resolve_board_path(path: str) -> str:
    """
    Resolves the full path on the board by combining the drive letter with the provided path.

    Args:
        path (str): The relative path to the file or directory.

    Returns:
        str: The full path on the board.
    """
    return os.path.join(f'{BOARD_DRIVE_LETTER}', path)

@log_function_call
def copy_file(source: str, destination_path: str) -> str:
    """
    Copies a file from the source location to the specified destination on the board.

    Args:
        source (str): The path to the source file to be copied.
        destination_path (str): The destination path on the board.

    Returns:
        str: The destination path where the file was copied.
    """
    logger.info(f'Saving file to board: {source}')

    dest = resolve_board_path(destination_path)

    try:
        shutil.copy(source, dest)
        logger.info(f'File copied from {source} to {dest}')
    except FileNotFoundError as e:
        logger.error(f'File not found: {source}. Error: {e}')
    except PermissionError as e:
        logger.error(f'Permission denied when trying to copy to: {dest}. Error: {e}')
    except Exception as e:
        logger.error(f'Unexpected error occurred while copying file: {e}')

    return dest

@log_function_call
def write_file(destination_path: str) -> None:
    """
    Creates or overwrites a file at the specified destination on the board.

    Args:
        destination_path (str): The path where the file will be created or overwritten.
    """
    dest = resolve_board_path(destination_path)

    logger.info(f'Writing to file on board: {dest}')
    
    try:
        with open(dest, 'w') as f:
            f.write('')
            logger.info(f'Successfully wrote to file: {dest}')
    except FileNotFoundError as e:
        logger.error(f'The destination path does not exist: {dest}. Error: {e}')
    except PermissionError as e:
        logger.error(f'Permission denied when writing to: {dest}. Error: {e}')
    except Exception as e:
        logger.error(f'Unexpected error occurred while writing to the file: {e}')

@log_function_call
def append(destination_path: str, text: str) -> None:
    """
    Appends text to the specified file on the board.

    Args:
        destination_path (str): The path to the file to which the text will be appended.
        text (str): The text to append to the file.
    """
    dest = resolve_board_path(destination_path)

    logger.info(f'Appending {text} to file on board: {dest}')
    
    try:
        with open(dest, 'a') as f:
            f.write(text + '\n')
            logger.info(f'Successfully appended to file: {dest}')
    except FileNotFoundError as e:
        logger.error(f'The destination path does not exist: {dest}. Error: {e}')
    except PermissionError as e:
        logger.error(f'Permission denied when appending to: {dest}. Error: {e}')
    except Exception as e:
        logger.error(f'Unexpected error occurred while appending to the file: {e}')

@log_function_call
def create_or_update_log(text: str) -> None:
    """
    Creates a log file if it doesn't exist and appends the specified text.

    Args:
        text (str): The text to write to the log file.
    """
    log_file_path = resolve_board_path(LOG_FILENAME)

    try:
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))
            logger.info(f'Created directories for log file path: {os.path.dirname(log_file_path)}')
    
        append(log_file_path, text)
    except Exception as e:
        logger.error(f'Failed to create or update log file: {log_file_path}. Error: {e}')
