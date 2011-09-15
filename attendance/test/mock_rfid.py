# mock_rfid.py - A mock object to stand in for an RFID reader.

class MockRfid(object):
    def __init__(self):
        self.calls = {}
        self.handlers = {}

    def openPhidget(self):
        pass

    def waitForAttach(self, timeout):
        pass

    def setAntennaOn(self, on):
        pass

    def setOnTagHandler(self, handler):
        self.handlers['ontag'] = handler

    def send_tag_event(self):
        evt = MockEvent(MockDevice())
        self.handlers['ontag'](evt)

class MockEvent(object):
    def __init__(self, device):
        self.device = device
        
class MockDevice(object):
    def __init__(self):
        pass

    def getSerialNum(self):
        return 1234
