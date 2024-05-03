# from smbus2 import SMBus
import time, json, threading, os, importlib

from utils.logger import export_loggers, setup_logger

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
def read_data_from_component(name, bus):
    """
    Read I2C bus for a specified component
    name (str) : The component name
    bus (SMBus) : The I2C bus to read from
    """
    global running

    while running:
        try:
            comp_module = importlib.import_module(f"readers.{name}")
            timeout = comp_module.read_bus(bus)
            time.sleep(timeout)

        except KeyboardInterrupt:  # Quitting
            running = False

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

    # --------------------------------- Main Loop -------------------------------- #

    while running:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:  # Quitting
            print("\nQuitting...")
            running = False

            # Stopping threads
            for name in threads:
                threads[name].join()

            # Closing I2C bus
            # TODO: Uncomment bus closing
            # bus.close()