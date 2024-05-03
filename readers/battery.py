import json, logging

# ----------------------------- Config / Loggers ----------------------------- #

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
comp_config = config['components']['battery']

logger = logging.getLogger('battery')

ADDR = comp_config['addr']
TIMEOUT = comp_config['timeout']
ERR_TIMEOUT = comp_config['err_timeout']

# ------------------------------- Read function ------------------------------ #

def read_bus(bus):
    # Get data from the bus
    try:
        # TODO: Uncomment bus read line
        # data = bus.read_i2c_block_data(ADDR, 0, 16)
        data = [123, 34, 100, 97, 116, 97, 34, 58, 32, 51, 125]
    except:
        logger.error('remote i/o error')
        return ERR_TIMEOUT

    # Decode and clean
    logger.debug(data)
    data_str = "".join(map(chr, data))
    data_str = data_str.replace(chr(255), '')
    logger.debug(data_str)

    # Parse using JSON
    try:
        data_json = json.loads(data_str)
        logger.info(data_json)
    except json.decoder.JSONDecodeError:
        logger.error("JSON error")
        return ERR_TIMEOUT

    return TIMEOUT