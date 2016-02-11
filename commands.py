class OutputWriter:
    file = None

    def __init__(self, filename_out):
        file = open(filename_out, 'w')

    def writeLoad(self, droneId, warehouseId, productId, numProducts):
        file.write('{}L{}{}{}'.format(droneId, warehouseId, productId, numProducts))

    def writeUnload(self, droneId, warehouseId, productId, numProducts):
        file.write('{}U{}{}{}'.format(droneId, warehouseId, productId, numProducts))

    def writeDeliver(self, droneId, customerId, productId, numProducts):
        file.write('{}D{}{}{}'.format(droneId, customerId, productId, numProducts))

    def writeWait(self, droneId, numTimesteps):
        file.write('{}W{}'.format(droneId, numTimesteps))
