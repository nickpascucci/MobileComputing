# tracker.py - Attendance tracking daemon.

# Responsibilities:
# Interface with RFID reader and add hits to database.

import couchdb
import datetime
from Phidgets.Devices import RFID

TIME_FORMAT = "%Y%m%d%H%M%S"

class Tracker(object):
    """Handle RFID tag events and communicate with the CouchDB database."""

    def __init__(self, rfid, db):
        self.rfid = rfid
        self.db = db
        self.rfid.setOnTagHandler(self.on_tag)
        self.rfid.openPhidget()
        self.rfid.waitForAttach(10000)
        self.rfid.setAntennaOn(True)
        self.print_greeting()

    def on_tag(self, e):
        serial_number = e.device.getSerialNum()
        timestamp = self.get_timestamp()
        self.database_put(str(serial_number), timestamp)

    def database_put(self, serial, time):
        if not serial in self.db:
            self.database_create(serial, time)
        else:
            record = self.database_get(serial)
            self.greet_student(record["name"])
            record["timestamps"].append(time)
            self.db[serial] = record

    def database_create(self, serial, time):
        info = self.get_student_info()
        self.db[serial] = {"timestamps": [time],
                           "name":info[0],
                           "grade":info[1]}
        
    def database_get(self, serial):
        return self.db[serial]

    @staticmethod
    def greet_student(name):
        print "Hello again, %s! Good to see you." % name
    
    @staticmethod
    def get_student_info():
        print "Hello! I haven't met you yet."
        name = raw_input("What's your name?")
        print "Pleased to meet you, %s!" % name
        grade = raw_input("What grade are you in?")
        print "That's great. Have a nice day!"
        return (name, grade)

    @staticmethod
    def get_timestamp():
        timestamp = datetime.datetime.now().strftime(TIME_FORMAT)
        return timestamp

    @staticmethod
    def print_greeting():
        print "Tracker is online!"
        print "Now waiting for new IDs."

def main():
    db = couchdb.Server()["students"]
    rfid = RFID.RFID()
    Tracker(rfid, db)
    raw_input("Press Enter to exit.")
        
if __name__ == "__main__":
    main()
