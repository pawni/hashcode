import json
import sys
import numpy as np

data = {}

def getNumArray(inList):
    arr = []
    for item in inList:
        arr.append(int(item))
    return arr

with open(sys.argv[1]) as inFile:
    firstLineData = inFile.readline().strip().split(' ')
    data['numRows'] = int(firstLineData[0].strip())
    data['numCols'] = int(firstLineData[1].strip())
    data['numDrones'] = int(firstLineData[2].strip())
    data['numTurns'] = int(firstLineData[3].strip())
    data['maxPayload'] = int(firstLineData[4].strip())
    numProductTypes = int(inFile.readline().strip())
    data['numProductTypes'] = numProductTypes
    productWeights = getNumArray(inFile.readline().strip().split(' '))
    data['productWeights'] = productWeights

    numWarehouses = int(inFile.readline().strip())
    data['numWarehouses'] = numWarehouses

    warehousesData = []
    for i in range(numWarehouses):
        whData = {}
        coordinatesLine = inFile.readline().strip().split(' ')
        whData['x'] = int(coordinatesLine[0].strip())
        whData['y'] = int(coordinatesLine[1].strip())
        itemsLine = inFile.readline().strip().split(' ')
        #items = []
        #for item in itemsLine
        whData['items'] = getNumArray(itemsLine)
        warehousesData.append(whData)
    data['warehousesData'] = warehousesData
    numOrders = int(inFile.readline().strip())
    data['numOrders'] = numOrders
    orderData = []
    for i in range(numOrders):
        oData = {}
        coordinatesLine = inFile.readline().strip().split(' ')
        oData['x'] = int(coordinatesLine[0].strip())
        oData['y'] = int(coordinatesLine[1].strip())
        numItems = int(inFile.readline().strip())
        oData['numOrders'] = numItems
        itemsLine = inFile.readline().strip().split(' ')
        oData['items'] = getNumArray(itemsLine)
        orderItems = []
        for j in range(numProductTypes):
            orderItems.append(np.sum(np.array(oData['items']) == j))
        oData['itemsList'] = orderItems
        orderData.append(oData)

    data['orderData'] = orderData

#print data

outFile = open(sys.argv[1] + '.json', 'wb')
json = json.dump(data, outFile)

'''
with open(sys.argv[1] + '.json', 'wb') as outFile:
    print >> outFile, json
'''
