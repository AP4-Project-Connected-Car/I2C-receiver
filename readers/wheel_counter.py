import json, logging

# ----------------------------- Config / Loggers ----------------------------- #

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
comp_config = config['components']['wheel_counter']

logger = logging.getLogger('wheel_counter')

ADDR = comp_config['addr']
TIMEOUT = comp_config['timeout']
ERR_TIMEOUT = comp_config['err_timeout']

# ------------------------------- Read function ------------------------------ #

def read_bus(bus, wsc):
    if wsc is None:
        return ERR_TIMEOUT
        
    # Get data from the bus
    try:
        data = bus.read_i2c_block_data(ADDR, 0, 16)
        logger.debug(data)
    except:
        logger.error('remote i/o error')
        return ERR_TIMEOUT

    # Decode and clean
    data_str = "".join(map(chr, data))
    data_str = data_str.replace(chr(255), '')

    # Parse using JSON
    try:
        data_json = json.loads(data_str)
        to_send = {
            'for': 'server',
            'component': 'wheelCounter',
            'content': {
                'value': data_json['data']
            }
        }
        logger.info(json.dumps(to_send))

        # Send the data to the server
        wsc.send(json.dumps(to_send))
    except json.decoder.JSONDecodeError:
        logger.error("JSON error")
        return ERR_TIMEOUT

    return TIMEOUT