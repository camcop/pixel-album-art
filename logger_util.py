import logging
from functools import wraps
from typing import Callable, Optional, Any

# Logger configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def log_function_call(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Optional[str]:
        try:
            logger.info(f'Calling function {func.__name__} with arguments: {args}, {kwargs}')
            result = func(*args, **kwargs)
            logger.info(f'Function {func.__name__} completed successfully')
            return result
        except Exception as e:
            logger.error(f'Error in function {func.__name__}: {e}')
            return None
    return wrapper
