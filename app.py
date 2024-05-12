# TODO: Uncomment bus library import
# from smbus2 import SMBus
import time, json, threading, os, importlib, websocket

from utils.logger import export_loggers, setup_logger
from utils.ws import on_message, on_error, on_close
# ----------------------------- Config / Loggers ----------------------------- #

# Import config
with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())

# Setup loggers
I2C_DEBUG_LOG = bool(int(os.environ.get('I2C_DEBUG_LOG', True)))
main_logger = setup_logger('app', debug=I2C_DEBUG_LOG)
component_loggers = export_loggers(I2C_DEBUG_LOG)

# --------------------------- Threads main function -------------------------- #

running = True
wsc = None
def read_data_from_component(name, bus):
    """
    Read I2C bus for a specified component
    name (str) : The component name
    bus (SMBus) : The I2C bus to read from
    """
    global running, wsc

    while running:
        try:
            # Import and run the component read function
            comp_module = importlib.import_module(f"readers.{name}")
            timeout = comp_module.read_bus(bus, wsc)

            # Wait before read again
            time.sleep(timeout)

        except KeyboardInterrupt:  # Quitting
            running = False

def on_open(ws):
    """ When the WS client is connected """
    global wsc
    
    main_logger.info("WS connection opened !")
    wsc = ws

# ---------------------------------------------------------------------------- #
#                                 Main content                                 #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":

    # ------------------------------- Init threads ------------------------------- #

    # TODO: Uncomment bus init
    # Init I2C bus (/dev/ic2-1)
    # bus = SMBus(1) 

    # Creating threads for each address
    threads = {}
    for name in config['components']:
        # TODO: Add bus param
        threads[name] = threading.Thread(target=read_data_from_component, args=(name, None))

    # Starting threads
    for name in threads:
        threads[name].start()

    # --------------------------- Init WebSocket client -------------------------- #

    ws = websocket.WebSocketApp(config['ws']['uri'], on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    # --------------------------------- Main Loop -------------------------------- #

    try:
        ws.run_forever()
    except:  # Quitting
        print("\nQuitting...")
        running = False

        # Stopping threads
        for name in threads:
            threads[name].join()

        # Closing I2C bus
        # TODO: Uncomment bus closing
        # bus.close()