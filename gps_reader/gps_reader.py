import pynmea2 # install this module using command in the terminal "pip install pynmea2"
from datetime import datetime, timedelta, timezone # pre-installed library

class GPSReader:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.speed = None
        self.utc_time = None
        self.local_time = None
        self.status = None
        self.date = None

    def get_zone_time(self, utc_time):
        """
        Convert UTC time to local time using a predefined time zone offset.
        Modify the offset as per your local time zone.
        """
        local_offset = timedelta(hours=5, minutes=30)  # Change this for other zones
        local_time = utc_time + local_offset
        return local_time

    def parse_gps_data(self, line):
        """
        Parse and extract individual GPS data parameters.
        """
        try:
            msg = pynmea2.parse(line)

            if msg.sentence_type == "RMC":
                # Extract and store data
                self.utc_time = datetime.combine(datetime.now(timezone.utc).date(), msg.timestamp)
                self.local_time = self.get_zone_time(self.utc_time)
                self.status = 'Active' if msg.status == 'A' else 'Void'
                self.latitude = msg.latitude
                self.longitude = msg.longitude
                self.speed = msg.spd_over_grnd
                self.date = msg.datestamp

                return True  # Successfully parsed and updated the data
            return False
        except pynmea2.ParseError as e:
            print(f"Error parsing data: {e}")
            return False

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_speed(self):
        return self.speed

    def get_utc_time(self):
        return self.utc_time

    def get_local_time(self):
        return self.local_time

    def get_status(self):
        return self.status

    def get_date(self):
        return self.date
