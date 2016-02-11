class OutputWriter:

    def __init__(self, filename_out):
        self.filename_out = filename_out
        self.file = open(filename_out, 'w')

    def writeLoad(self, droneId, warehouseId, productId, numProducts):
        self.file.write('{} L {} {} {}\n'.format(droneId, warehouseId, productId, numProducts))

    def writeUnload(self, droneId, warehouseId, productId, numProducts):
        self.file.write('{} U {} {} {}\n'.format(droneId, warehouseId, productId, numProducts))

    def writeDeliver(self, droneId, customerId, productId, numProducts):
        self.file.write('{} D {} {} {}\n'.format(droneId, customerId, productId, numProducts))

    def writeWait(self, droneId, numTimesteps):
        self.file.write('{} W {}\n'.format(droneId, numTimesteps))

    def endFile(self):
        count = 0
        with open(self.filename_out, 'r+') as f:
            for i, l in enumerate(f):
                pass
            count = i+1

        with open(self.filename_out, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(count.rstrip('\r\n') + '\n' + content)
