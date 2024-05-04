import socket
import json
from pymodbus.client import ModbusTcpClient
# import RPi.GPIO as GPIO
import time
import BRXPython
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT)



class PLCTag():
    def __init__(self, name, modbus_address, value):
        self.name = name
        self.modbus_address = modbus_address
        self.value = value


def write_modbus_coils(client, coil_address, value):

    result = None
    # Take care of the offset between pymodbus and the click plc
    coil_address = coil_address - 1

    # pymodbus built in write coil function
    result = client.write_coil(coil_address, value)

    return result


def read_modbus_coils(client, coil_address, number_of_coils=1):
    # Predefining a empty list to store our result
    result_list = []

    # Take care of the offset between pymodbus and the click plc
    coil_address = coil_address - 1

    # Read the modbus address values form the click PLC
    result = client.read_coils(coil_address, number_of_coils)

    # print("Response from PLC with pymodbus library", result.bits)

    # storing our values form the plc in a list of length
    # 0 to the number of coils we want to read
    result_list = result.bits[0:number_of_coils]

    # print("Filtered result of only necessary values", result_list)
    return result_list



def connect_to_click_plc():
    click_ip_address = '192.168.2.23'
    # Attempting to create connection to click PLC
    # Return client object for other functions

    print("Attempting to connect to PLC")

    # Creating a client object with the parameters of the PLC IP and Port
    click_plc_obj = ModbusTcpClient(click_ip_address, port='502')

    # Attempt to connect to the PLC
    click_plc_obj.connect()
    print("connected to PLC")

    # Return our PLC object
    return click_plc_obj


def disconnect_from_click_plc(client):
    print("Disconnecting from click PLC")
    client.close()

def write_to_json_file(filename, data_dict):
    with open(filename, "w") as file:
        json.dump(data_dict, file)

def main():
    
    client = connect_to_click_plc()
    # Define server IP address and port
    server_ip = '0.0.0.0'  # Replace with your Raspberry Pi's IP address
    server_port = 5001

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address
    server_socket.bind((server_ip, server_port))
    print('server port =', server_port)

    # Listen for incoming connections
    server_socket.listen(2)

    print("Server is listening for incoming connections...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()

        try:
            print("Connection established with:", client_address)

            # Receive data from the client
            while True:
                data = connection.recv(1024)

                if data:
                    status = data.decode()
                    print("Received:", status)
                    # GPIO.output(18, False)
                    BRXPython.main(status)

                else:
                    break

        finally:
            # Clean up the connection
            connection.close()


if __name__ == '__main__':
    main()
