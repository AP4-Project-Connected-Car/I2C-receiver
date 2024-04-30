from smbus2 import SMBus
import time, json, threading

def read_data_from_address(address):
    while True:
        try:
            data = bus.read_i2c_block_data(address, 0, 16)
            print(f"received from slave {address}:")
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

        except KeyboardInterrupt:  # Quitting
            break

ADDR = 11  # bus address
ADDR2 = 12  # bus address
bus = SMBus(1)  # indicates /dev/ic2-1

print("I2C test with Python :")

# Creating threads for each address
thread1 = threading.Thread(target=read_data_from_address, args=(ADDR,))
thread2 = threading.Thread(target=read_data_from_address, args=(ADDR2,))

# Starting threads
thread1.start()
thread2.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:  # Quitting
    print("\nQuitting...")
    thread1.join()
    thread2.join()
    bus.close()
