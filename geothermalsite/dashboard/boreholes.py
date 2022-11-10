### start and end laf for each of the boreholes

borehole1_data = []
borehole2_data = []
borehole3_data = []
borehole4_data = []
borehole5_data = []

class Borehole(object):
    def __init__(self, borehole = None):
        self.setValues(borehole)
        self.start = 0
        self.bottom = 0
        self.end = 0
        self.channel = 0

    def getStart(self):
        return self.start

    def getBottom(self):
        return self.bottom
    
    def getEnd(self):
        return self.end
    
    def getChannel(self):
        return self.channel

    def setValues(self, borehole):
        self.start = borehole[0]
        self.bottom = borehole[1]
        self.end = borehole[2]
        self.channel = borehole[3]


borehole1 = Borehole[borehole1_data]
borehole2 = Borehole[borehole2_data]
borehole3 = Borehole[borehole3_data]
borehole4 = Borehole[borehole4_data]
borehole5 = Borehole[borehole5_data]

