class OutputWriter:
    file = None

    def __init__(self, filename_out):
        file = open(filename_out, 'w')

    def writeLoad(self, droneId, warehouseId, productId, numProducts):
        file.write('{}L{}{}{}\n'.format(droneId, warehouseId, productId, numProducts))

    def writeUnload(self, droneId, warehouseId, productId, numProducts):
        file.write('{}U{}{}{}\n'.format(droneId, warehouseId, productId, numProducts))

    def writeDeliver(self, droneId, customerId, productId, numProducts):
        file.write('{}D{}{}{}\n'.format(droneId, customerId, productId, numProducts))

    def writeWait(self, droneId, numTimesteps):
        file.write('{}W{}\n'.format(droneId, numTimesteps))

