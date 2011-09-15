# tracker_test.py - Unit tests for tracker.py

import unittest
from MobileComputing.attendance import tracker
from MobileComputing.attendance.test import mock_rfid

class TrackerTest(unittest.TestCase):
    def setUp(self):
        self.db = {} # CouchDB in Python is essentially a dictionary. Mock it!
        self.rfid = mock_rfid.MockRfid()
        self.tracker = tracker.Tracker(self.rfid, self.db)
        
    def tearDown(self):
        pass

    # Test when RFID of extant user is read, writes timestamp
    def testWritesTimestampOnRead(self):
        self.db["12345"] = {"timestamps": [1234], "name":"Sally"}
        self.rfid.send_tag_event()
        items = len(self.db["12345"]["timestamps"])
        assert items is 2

    def testCreatesRecordForNewTag(self):
        def new_get_student_info():
            return ("Sally", 12)
        self.tracker.get_student_info = new_get_student_info
        self.rfid.send_tag_event()
        assert self.tracker.db["12345"] is not None


if __name__ == "__main__":
    unittest.main()
