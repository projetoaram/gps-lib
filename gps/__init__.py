import serial as lib

class GPS:

    GGA = 0
    GSA = 1
    GSV = 2
    RMC = 3

    def __init__(self, baudrate=9600, port="/dev/ttyAMA0"):
        try:
            self.serial = lib.Serial(port, baudrate, timeout=3)

            if not self.serial.isOpen():
                self.serial.open()
        except:
            print("[GPS] Unexpected error: Could not stablish GPS connection.")
            raise

    def read(self):
        self._read(self.GGA)
        self._read(self.RMC)

    def _read(self, nmea):
        try:
            self.serial.flushInput()
            self.serial.flushOutput()
        except:
            print("[GPS] Unexpected error: Could not flush data. Check if GPS is connected.")
            raise

        if nmea == self.GGA:
            sufix = "$GPGGA"
        elif nmea == self.GSA:
            sufix = "$GPGSA"
        elif nmea == self.GSV:
            sufix = "$GPGSV"
        elif nmea == self.RMC:
            sufix = "$GPRMC"
        else:
            print "Not found NMEA!"
            return

        try:
            line = self.serial.readline()

            # Strings for testing without GPS
            # if nmea == self.GGA:
            #     line = "$GPGGA,190000.000,0549.9510,S,03512.3255,W,1,6,2.45,45.0,M,-10.0,M,,*45" # CIVT
            # elif nmea == self.RMC:
            #     line = "$GPRMC,190000,A,0549.9510,S,03512.3255,W,173.8,231.8,280415,004.2,W*70" # CIVT
        except:
            print("[GPS] Unexpected error: Could not read data. Check if GPS is connected.")
            raise

        if line == "":
            print "[GPS] Unexpected error: GPS not connected or could not found satellites."
            return

        while(line[:6] != sufix):
            try:
                line = self.serial.readline()
            except:
                print("[GPS] Unexpected error: Could not read data. Check if GPS is connected.")
                raise

        values = line.split(",")
        if nmea == self.GGA:
            self._quality = int(values[6])

            if self._quality != 0:
                self._lat_indicator = values[3]
                aux_lat = values[2].split(".")
                degrees_lat = int((aux_lat[0])[:-2])
                str_minutes_lat = (aux_lat[0])[-2:]
                str_seconds2minutes_lat = aux_lat[1]
                minutes_lat = float(str_minutes_lat + "." + str_seconds2minutes_lat)

                self._lat = degrees_lat + minutes_lat/60.0
                if self._lat_indicator == 'S' or self._lat_indicator == 's':
                    self._lat *= -1

                self._lon_indicator = values[5]
                aux_lon = values[4].split(".")
                degrees_lon = int((aux_lon[0])[:-2])
                str_minutes_lon = (aux_lon[0])[-2:]
                str_seconds2minutes_lon = aux_lon[1]
                minutes_lon = float(str_minutes_lon + "." + str_seconds2minutes_lon)

                self._lon = degrees_lon + minutes_lon/60.0
                if self._lon_indicator == 'W' or self._lon_indicator == 'w':
                    self._lon *= -1

                self._elevation = float(values[9])
            else:
                print "[GPS] Unexpected error: Low quality signal. Impossible to read data."
                return

        elif nmea == self.RMC:
            str_time = values[1]
            str_date = values[9]

            temp_str_datetime = "%s/%s/%s %s:%s:%s" % (str_date[:2], str_date[2:4], str_date[4:6], str_time[:2], str_time[2:4], str_time[4:6])
            self._date = temp_str_datetime

    @property
    def date(self):
        return self._date

    @property
    def lat(self):
        return self._lat

    @property
    def lat_indicator(self):
        return self._lat_indicator

    @property
    def lon(self):
        return self._lon

    @property
    def lon_indicator(self):
        return self._lon_indicator

    @property
    def quality(self):
        return self._quality

    @property
    def elevation(self):
        return self._elevation

    def close(self):
        try:
            if self.serial.isOpen():
                self.serial.close()
        except:
            print("[GPS] Unexpected error: Could not stablish GPS connection.")
            raise
