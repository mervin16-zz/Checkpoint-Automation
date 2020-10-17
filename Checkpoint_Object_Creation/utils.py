import logging


def create_logger(path):
    """ How to call this function?
    
    from utils import create_logger
    from datetime import datetime
    import os
    
    # log folder path
    LOG_FOLDER = os.path.join(os.path.dirname(__file__), 'log/')

    # create log folder 
    if os.path.exists(LOG_FOLDER) is False:
        os.mkdir(LOG_FOLDER)

    logger = create_logger((LOG_FOLDER + datetime.now().strftime("%Y-%m-%d--%H:%M:%S") + '.log'))

    # Display a message on console and in file
    logger.info("TEST") 

    # Display a message only in file
    logger.debug("TEST")
    """

    logger = logging.getLogger()

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(path)

    # Create formatters and add it to handlers
    f_format = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
    )

    f_handler.setFormatter(f_format)

    # Set logging level
    logger.setLevel(logging.DEBUG)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
