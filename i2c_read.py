from smbus2 import SMBus
import time, json

ADDR = 11 # bus address
ADDR2 = 12 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

print("I2C test with Python :")
running = True
while running:
    try:

        data= bus.read_i2c_block_data(ADDR, 0, 16)
        print("received from slave:")
        print(data)
        data_str = "".join(map(chr, data))
        print(data_str)
        data_str = data_str.replace(chr(255), '')
        print(data_str)
        data_json = json.loads(data_str)
        print(data_json)
        print(data_json['data'])
        time.sleep(1)

    except json.decoder.JSONDecodeError:
        print("ERROR JSON")
        time.sleep(1)

    except KeyboardInterrupt: # Quitting
        running = False

# Stopping
print("")
print("Quitting...")
bus.close()
