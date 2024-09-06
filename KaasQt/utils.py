import time
import logging
from functools import wraps

def measure_loading_time(func):
    """
    Decorator to measure the loading time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        loading_time = end_time - start_time
        logging.info(f"Loading time for {func.__name__}: {loading_time:.2f} seconds")
        return result
    return wrapper

def setup_logging():
    """
    Set up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='kaas_app.log',
        filemode='a'
    )

    # Add a stream handler to print log messages to the console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

def log_exception(e):
    """
    Log an exception with its traceback.
    """
    logging.exception(f"An error occurred: {str(e)}")