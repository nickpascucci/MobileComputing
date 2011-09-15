# analyze.py - Analyze attendance

import couchdb
import datetime
from MobileComputing.attendance.tracker import TIME_FORMAT

db = couchdb.Server()['students']

start_time = raw_input("Ok, let's get started. When does class begin? (HH:MM) ")
start_time = datetime.datetime.strptime(start_time, "%H:%M").time()

def pretty_print(data):
    print ("Name: %(Name)s\n"
           "Grade: %(Grade)s\n"
           "Late Days: %(Late)s\n"
           "On Time Days: %(On Time)s\n") % data

def is_after(first, second):
    """Return true if first is after second."""
    return first > second

print "Looking up data."
for rfid_tag in db:
    record = db[rfid_tag]
    student_data = {}
    student_data["Serial Number"] = rfid_tag
    student_data["Name"] = record["name"]
    student_data["Grade"] = record["grade"]
    student_data["Late"] = 0
    student_data["On Time"] = 0
    for timestamp in record["timestamps"]:
        ts_date = datetime.datetime.strptime(timestamp, TIME_FORMAT)
        if is_after(ts_date.time(), start_time):
            student_data["Late"] += 1
        else:
            student_data["On Time"] += 1
        # Ideally, we'd have some way of checking if a student was entirely
        # absent. However, without knowing what days we're checking for, we
        # can't really do so...
    pretty_print(student_data)
