import serial  # install this module using command in the terminal "pip install pyserial"
from gps_reader import GPSReader

# Serial port and baud rate
SERIAL_PORT = "COM16"  # Com port where the GPS Module is connected
BAUD_RATE = 9600  # Default baud rate for many GPS modules

# Initialize GPSReader
gps_reader = GPSReader()

# Establish serial connection
try:
    gps_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening to GPS data on {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error connecting to GPS: {e}")
    gps_serial = None

# Read data continuously
try:
    while gps_serial and gps_serial.is_open:
        if gps_serial.in_waiting > 0:
            line = gps_serial.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$'):
                # Parse the GPS data
                if gps_reader.parse_gps_data(line):
                    # Access and print individual parameters from GPSReader
                    print(f"Time (UTC): {gps_reader.get_utc_time().strftime('%H:%M:%S+00:00')}")
                    print(f"Zone Time: {gps_reader.get_local_time().strftime('%H:%M:%S')}")
                    print(f"Status: {gps_reader.get_status()}")
                    print(f"Latitude: {gps_reader.get_latitude()} N")
                    print(f"Longitude: {gps_reader.get_longitude()} E")
                    print(f"Speed (knots): {gps_reader.get_speed()}")
                    print(f"Date: {gps_reader.get_date()}")
                    print(" ")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if gps_serial and gps_serial.is_open:
        gps_serial.close()
        print("Disconnected from GPS.")
