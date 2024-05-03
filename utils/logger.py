import logging, json

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())

def setup_logger(name, level=logging.INFO, debug=False):
    """Set up a logger with the given name and level."""
    lvl = logging.DEBUG if debug else level
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    formatter = logging.Formatter('[%(name)s] %(asctime)s <%(levelname)s> %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def export_loggers(debug=False):
    """Export multiple loggers."""
    lvl = logging.DEBUG if debug else logging.INFO

    result = {}
    for name in config['components']:
        result[name] = setup_logger(name, lvl)
    
    return result


