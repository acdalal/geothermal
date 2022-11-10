### start and end laf for each of the boreholes

borehole1_data = [230.3, 388.8, 547.3, 1]
borehole2_data = [775.1, 933.6, 1092.1, 1]
borehole3_data = [1255.9, 1424.4, 1582.9, 1]
borehole4_data = [123.0, 291.5, 450.0, 3]
borehole5_data = [562.0, 730.5, 889.0, 3]


class Borehole(object):
    def __init__(self, borehole=None):
        if borehole:
            self.setValues(borehole)
        else:
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


borehole1 = Borehole(borehole1_data)
borehole2 = Borehole(borehole2_data)
borehole3 = Borehole(borehole3_data)
borehole4 = Borehole(borehole4_data)
borehole5 = Borehole(borehole5_data)

boreholes = {1: borehole1, 2: borehole2, 3: borehole3, 4: borehole4, 5: borehole5}
