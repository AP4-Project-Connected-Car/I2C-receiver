import logging, json, time

logger = logging.getLogger('app')

# Import the config file
with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())

def on_message(ws, message):
    logger.debug("Received WS message: %s", message)

def on_error(ws, error):
    logger.error("WS error: %s", error)

def on_close(ws, close_status_code, close_msg):
    logger.warning("WS connection closed !")

    exit(1)