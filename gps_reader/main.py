import serial
import pynmea2
from datetime import datetime, timedelta, timezone

def get_zone_time(utc_time):
    """
    Convert UTC time to local time using a predefined time zone offset.
    Modify the offset as per your local time zone.
    """
    # Define your local time zone offset (e.g., +5:30 for IST)
    local_offset = timedelta(hours=5, minutes=30)  # Change this for other zones
    local_time = utc_time + local_offset
    return local_time

def parse_gps_data(line):
    """
    Parse and display decoded GPS data in a human-readable format.
    """
    try:
        msg = pynmea2.parse(line)

        if msg.sentence_type == "GGA":
            print("\nGPS Fix Data:")
            print(f"  Time (UTC): {msg.timestamp}")
            if msg.timestamp:
                utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                local_time = get_zone_time(utc_time)
                print(f"  Zone Time: {local_time.strftime('%H:%M:%S')} (Local)")

        elif msg.sentence_type == "RMC":
            print("\nRecommended Minimum Navigation Data:")
            print(f"  Time (UTC): {msg.timestamp}")
            if msg.timestamp:
                utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                local_time = get_zone_time(utc_time)
                print(f"  Zone Time: {local_time.strftime('%H:%M:%S')} (Local)")
            print(f"  Status: {'Active' if msg.status == 'A' else 'Void'}")
            print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
            print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
            print(f"  Speed (knots): {msg.spd_over_grnd}")
            print(f"  Date: {msg.datestamp}")

        elif msg.sentence_type == "GSA":
            print("\nSatellite Status:")
            print(f"  Mode: {msg.mode}")
            print(f"  Fix Type: {msg.mode_fix_type}")
            try:
                satellites_used = getattr(msg, 'sv_id', None)
                if satellites_used:
                    print(f"  Satellites Used: {', '.join(filter(None, satellites_used))}")
                else:
                    print("  Satellites Used: Not available")
            except AttributeError:
                print("  Satellites Used: Not available")
            print(f"  PDOP: {msg.pdop}, HDOP: {msg.hdop}, VDOP: {msg.vdop}")

        elif msg.sentence_type == "GSV":
            print("\nSatellites in View:")
            try:
                total_satellites = msg.data[2]  # Typically the total number of satellites is in the third field
                print(f"  Total Satellites: {total_satellites}")
                print(f"  Message Number: {msg.msg_num}/{msg.total_msgs}")
                satellite_info = msg.data[3:]  # Remaining data contains satellite information
                for i in range(0, len(satellite_info), 4):
                    print(f"    Satellite {i // 4 + 1}: ID={satellite_info[i]}, Elevation={satellite_info[i+1]}, Azimuth={satellite_info[i+2]}, SNR={satellite_info[i+3]}")
            except (IndexError, AttributeError) as e:
                print("  Satellite information not available.")

        elif msg.sentence_type == "GLL":
            print("\nGeographic Position:")
            print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
            print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
            print(f"  Time (UTC): {msg.timestamp}")
            if msg.timestamp:
                utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                local_time = get_zone_time(utc_time)
                print(f"  Zone Time: {local_time.strftime('%H:%M:%S')} (Local)")
            print(f"  Status: {'Valid' if msg.status == 'A' else 'Invalid'}")

        elif msg.sentence_type == "VTG":
            print("\nCourse Over Ground and Ground Speed:")
            print(f"  True Track: {msg.true_track}°")
            print(f"  Magnetic Track: {msg.mag_track}°")
            print(f"  Speed (knots): {msg.spd_over_grnd_kts}")
            print(f"  Speed (km/h): {msg.spd_over_grnd_kmph}")

        else:
            print(f"\nUnhandled Message ({msg.sentence_type}):")
            print(msg)
    except pynmea2.ParseError as e:
        print(f"Could not parse the line: {line}")
        print(f"Error: {e}")



def read_and_decode_gps(serial_port, baud_rate):
    """
    Read GPS data from a serial port and decode it.
    """
    try:
        gps_serial = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Listening to GPS data on {serial_port} at {baud_rate} baud.")

        while True:
            if gps_serial.in_waiting > 0:
                line = gps_serial.readline().decode('ascii', errors='ignore').strip()
                if line.startswith('$'):
                    parse_gps_data(line)
                    print("/////////////////////////////////////////////////////////////////////")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if gps_serial.is_open:
            gps_serial.close()
            print("Serial connection closed.")


if __name__ == "__main__":
    # Replace with your GPS module's serial port and baud rate
    SERIAL_PORT = "COM16"  # Example for Windows
    BAUD_RATE = 9600  # Default baud rate for many GPS modules

    read_and_decode_gps(SERIAL_PORT, BAUD_RATE)




# import serial
# import pynmea2
#
#
# def parse_gps_data(line):
#     """
#     Parse and display decoded GPS data in a human-readable format.
#     """
#     try:
#         msg = pynmea2.parse(line)
#
#         if msg.sentence_type == "GGA":
#             print("\nGPS Fix Data:")
#             print(f"  Time (UTC): {msg.timestamp}")
#             print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
#             print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
#             print(f"  Fix Quality: {msg.gps_qual}")
#             print(f"  Number of Satellites: {msg.num_sats}")
#             print(f"  Altitude: {msg.altitude} {msg.altitude_units}")
#
#         elif msg.sentence_type == "RMC":
#             print("\nRecommended Minimum Navigation Data:")
#             print(f"  Time (UTC): {msg.timestamp}")
#             print(f"  Status: {'Active' if msg.status == 'A' else 'Void'}")
#             print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
#             print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
#             print(f"  Speed (knots): {msg.spd_over_grnd}")
#             print(f"  Date: {msg.datestamp}")
#
#         elif msg.sentence_type == "GSA":
#             print("\nSatellite Status:")
#             print(f"  Mode: {msg.mode}")
#             print(f"  Fix Type: {msg.mode_fix_type}")
#             try:
#                 satellites_used = getattr(msg, 'sv_id', None)
#                 if satellites_used:
#                     print(f"  Satellites Used: {', '.join(filter(None, satellites_used))}")
#                 else:
#                     print("  Satellites Used: Not available")
#             except AttributeError:
#                 print("  Satellites Used: Not available")
#             print(f"  PDOP: {msg.pdop}, HDOP: {msg.hdop}, VDOP: {msg.vdop}")
#
#         elif msg.sentence_type == "GSV":
#             print("\nSatellites in View:")
#             try:
#                 total_satellites = msg.data[2]  # Typically the total number of satellites is in the third field
#                 print(f"  Total Satellites: {total_satellites}")
#                 print(f"  Message Number: {msg.msg_num}/{msg.total_msgs}")
#                 satellite_info = msg.data[3:]  # Remaining data contains satellite information
#                 for i in range(0, len(satellite_info), 4):
#                     print(f"    Satellite {i // 4 + 1}: ID={satellite_info[i]}, Elevation={satellite_info[i+1]}, Azimuth={satellite_info[i+2]}, SNR={satellite_info[i+3]}")
#             except (IndexError, AttributeError) as e:
#                 print("  Satellite information not available.")
#
#         elif msg.sentence_type == "GLL":
#             print("\nGeographic Position:")
#             print(f"  Latitude: {msg.latitude} {msg.lat_dir}")
#             print(f"  Longitude: {msg.longitude} {msg.lon_dir}")
#             print(f"  Time (UTC): {msg.timestamp}")
#             print(f"  Status: {'Valid' if msg.status == 'A' else 'Invalid'}")
#
#         elif msg.sentence_type == "VTG":
#             print("\nCourse Over Ground and Ground Speed:")
#             print(f"  True Track: {msg.true_track}°")
#             print(f"  Magnetic Track: {msg.mag_track}°")
#             print(f"  Speed (knots): {msg.spd_over_grnd_kts}")
#             print(f"  Speed (km/h): {msg.spd_over_grnd_kmph}")
#
#         else:
#             print(f"\nUnhandled Message ({msg.sentence_type}):")
#             print(msg)
#     except pynmea2.ParseError as e:
#         print(f"Could not parse the line: {line}")
#         print(f"Error: {e}")
#
#
#
# def read_and_decode_gps(serial_port, baud_rate):
#     """
#     Read GPS data from a serial port and decode it.
#     """
#     try:
#         gps_serial = serial.Serial(serial_port, baud_rate, timeout=1)
#         print(f"Listening to GPS data on {serial_port} at {baud_rate} baud.")
#
#         while True:
#             if gps_serial.in_waiting > 0:
#                 line = gps_serial.readline().decode('ascii', errors='ignore').strip()
#                 if line.startswith('$'):
#                     parse_gps_data(line)
#                     print("////////////////////////////////////////////////////////////////////////////////////////////////////////")
#     except serial.SerialException as e:
#         print(f"Serial error: {e}")
#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         if gps_serial.is_open:
#             gps_serial.close()
#             print("Serial connection closed.")
#
#
# if __name__ == "__main__":
#     # Replace with your GPS module's serial port and baud rate
#     SERIAL_PORT = "COM16"  # Example for Windows
#     BAUD_RATE = 9600  # Default baud rate for many GPS modules
#
#     read_and_decode_gps(SERIAL_PORT, BAUD_RATE)