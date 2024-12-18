import serial
import pynmea2
from datetime import datetime, timedelta, timezone

class GPSReader:
    def __init__(self, serial_port, baud_rate, local_offset_hours=5, local_offset_minutes=30):
        """
        Initialize the GPSReader object with serial port, baud rate, and local time offset.
        """
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.local_offset = timedelta(hours=local_offset_hours, minutes=local_offset_minutes)
        self.gps_serial = None

    def connect(self):
        """
        Establish a connection to the GPS module.
        """
        try:
            self.gps_serial = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"Connected to GPS on {self.serial_port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to GPS: {e}")
            self.gps_serial = None

    def disconnect(self):
        """
        Close the connection to the GPS module.
        """
        if self.gps_serial and self.gps_serial.is_open:
            self.gps_serial.close()
            print("Disconnected from GPS.")

    def convert_to_local_time(self, utc_time):
        """
        Convert UTC time to local time using the predefined time zone offset.
        """
        return utc_time + self.local_offset

    def parse_and_display(self, line):
        """
        Parse the GPS data line and display relevant information.
        """
        try:
            msg = pynmea2.parse(line)

            if msg.sentence_type == "GGA":
                print("\nGPS Fix Data:")
                print(f"  Time (UTC): {msg.timestamp}")
                if msg.timestamp:
                    utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                    local_time = self.convert_to_local_time(utc_time)
                    print(f"  Zone Time: {local_time.strftime('%H:%M:%S')} (Local)")

            elif msg.sentence_type == "RMC":
                print("\nRecommended Minimum Navigation Data:")
                print(f"  Time (UTC): {msg.timestamp}")
                if msg.timestamp:
                    utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                    local_time = self.convert_to_local_time(utc_time)
                    print(f"  Zone Time: {local_time.strftime('%H:%M:%S')} (Local)")
                print(f"  Status: {'Active' if msg.status == 'A' else 'Void'}")
                print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
                print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
                print(f"  Speed (knots): {msg.spd_over_grnd}")
                print(f"  Date: {msg.datestamp}")

            # Other message types can be handled similarly as in the procedural example
            else:
                print(f"\nUnhandled Message ({msg.sentence_type}):")
                print(msg)
        except pynmea2.ParseError as e:
            print(f"Could not parse the line: {line}")
            print(f"Error: {e}")

    def read_data(self):
        """
        Read data continuously from the GPS module.
        """
        if not self.gps_serial:
            print("GPS is not connected.")
            return

        try:
            print("Listening for GPS data...")
            while True:
                if self.gps_serial.in_waiting > 0:
                    line = self.gps_serial.readline().decode('ascii', errors='ignore').strip()
                    if line.startswith('$'):
                        self.parse_and_display(line)
                        print("/////////////////////////////////////////////////////////////////////")
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.disconnect()

if __name__ == "__main__":
    # Replace with your GPS module's serial port and baud rate
    SERIAL_PORT = "COM16"  # Example for Windows
    BAUD_RATE = 9600  # Default baud rate for many GPS modules

    gps_reader = GPSReader(SERIAL_PORT, BAUD_RATE)
    gps_reader.connect()
    gps_reader.read_data()


# import pynmea2
# from datetime import datetime, timedelta, timezone
#
#
# class GPSReader:
#     def __init__(self):
#         self.last_latitude = None
#         self.last_longitude = None
#
#     def get_zone_time(self, utc_time):
#         """
#         Convert UTC time to local time using a predefined time zone offset.
#         Modify the offset as per your local time zone.
#         """
#         # Define your local time zone offset (e.g., +5:30 for IST)
#         local_offset = timedelta(hours=5, minutes=30)  # Change this for other zones
#         local_time = utc_time + local_offset
#         return local_time
#
#     def parse_gps_data(self, line):
#         """
#         Parse and return decoded GPS data in a human-readable format.
#         """
#         try:
#             msg = pynmea2.parse(line)
#
#             if msg.sentence_type == "RMC":
#                 # Extract and format data
#                 utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
#                 local_time = self.get_zone_time(utc_time)
#
#                 # Check if the GPS position changed
#                 position_changed = False
#                 if self.last_latitude != msg.latitude or self.last_longitude != msg.longitude:
#                     self.last_latitude = msg.latitude
#                     self.last_longitude = msg.longitude
#                     position_changed = True
#
#                 if position_changed:
#                     decoded_data = f"""Time (UTC): {utc_time.strftime('%H:%M:%S+00:00')}
# Zone Time: {local_time.strftime('%H:%M:%S')}
# Status: {'Active' if msg.status == 'A' else 'Void'}
# Latitude: {msg.latitude} {msg.lat_dir}
# Longitude: {msg.longitude} {msg.lon_dir}
# Speed (knots): {msg.spd_over_grnd}
# Date: {msg.datestamp}"""
#                     return decoded_data
#
#             return None
#         except pynmea2.ParseError as e:
#             return f"Error parsing data: {e}"
#

# import serial
# import time
# from gps_reader import GPSReader
#
# class GPSConnection:
#     def __init__(self, serial_port, baud_rate):
#         self.serial_port = serial_port
#         self.baud_rate = baud_rate
#         self.gps_serial = None
#         self.gps_reader = GPSReader()
#
#     def connect(self):
#         """
#         Establish a connection to the GPS module.
#         """
#         try:
#             self.gps_serial = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
#             print(f"Listening to GPS data on {self.serial_port} at {self.baud_rate} baud.")
#         except serial.SerialException as e:
#             print(f"Error connecting to GPS: {e}")
#             self.gps_serial = None
#
#     def disconnect(self):
#         """
#         Close the connection to the GPS module.
#         """
#         if self.gps_serial and self.gps_serial.is_open:
#             self.gps_serial.close()
#             print("Disconnected from GPS.")
#
#     def read_data(self):
#         """
#         Read data continuously from the GPS module and pass to GPSReader for decoding.
#         """
#         if not self.gps_serial:
#             print("GPS is not connected.")
#             return
#
#         try:
#             while True:
#                 if self.gps_serial.in_waiting > 0:
#                     line = self.gps_serial.readline().decode('ascii', errors='ignore').strip()
#                     if line.startswith('$'):
#                         decoded_data = self.gps_reader.parse_gps_data(line)
#                         if decoded_data:
#                             # Print the data without additional gaps
#                             print(decoded_data)
#                             print(" ")
#         except KeyboardInterrupt:
#             print("\nExiting...")
#         finally:
#             self.disconnect()
#
# if __name__ == "__main__":
#     # Replace with your GPS module's serial port and baud rate
#     SERIAL_PORT = "COM16"  # Example for Windows
#     BAUD_RATE = 9600  # Default baud rate for many GPS modules
#
#     gps_connection = GPSConnection(SERIAL_PORT, BAUD_RATE)
#     gps_connection.connect()
#     gps_connection.read_data()