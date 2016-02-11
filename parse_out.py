import json
import sys
import numpy as np
import math

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

data_commands = {}

#with open(sys.argv[2]) as commandFile:
with sys.stdin as commandFile:
    numCommands = int(commandFile.readline().strip())
    data_commands['numCommands'] = numCommands

    drone_command = []
    for _ in range(data['numDrones']):
        drone_command.append([])
    for i in range(numCommands):
        commandLine = commandFile.readline().strip().split(' ')
        commandDict = {}
        if commandLine[1] == 'L': #load
            commandDict['type'] = 'L'
            commandDict['warehouse'] = int(commandLine[2].strip())
            commandDict['product'] = int(commandLine[3].strip())
            commandDict['number'] = int(commandLine[4].strip())

        elif commandLine[1] == 'D': # deliver
            commandDict['type'] = 'D'
            commandDict['order'] = int(commandLine[2].strip())
            commandDict['product'] = int(commandLine[3].strip())
            commandDict['number'] = int(commandLine[4].strip())
        elif commandLine[1] == 'W': #wait
            commandDict['type'] = 'W'
            commandDict['turns'] = int(commandLine[2].strip())
        elif commandLine[1] == 'U': # unload
            commandDict['type'] = 'U'
            commandDict['warehouse'] = int(commandLine[2].strip())
            commandDict['product'] = int(commandLine[3].strip())
            commandDict['number'] = int(commandLine[4].strip())
        drone_command[int(commandLine[0])].append(commandDict)
    data_commands['commands'] = drone_command

droneStates = []
droneCommandId = []
itemlist = []
for _ in range(data['numProductTypes']):
    itemlist.append(0)

for _ in range(data['numDrones']):
    droneCommandId.append(0)
    state = {}
    state['items'] = itemlist
    state['x'] = data['warehousesData'][0]['x']
    state['y'] = data['warehousesData'][0]['y']
    state['wait'] = 0
    state['payload'] = 0
    droneStates.append(state)

genetic = False

def getCommandString(command, dId):
    string = ""
    if command['type'] == 'W':
        string = "%d %s %d" %(dId, "W", command['turns'])
    elif command['type'] == 'D':
        string = "%d %s %d %d %d" %(dId, "W", command['order'], command['product'], command['number'])
    else:
        string = "%d %s %d %d %d" %(dId, command['type'], command['warehouse'], command['product'], command['number'])
    return string

def doInvalid(err, droneId=0):
    #print err
    #print 'invalid'
    droneCommandId[droneId] += 1

validMoves = []

score = 0
valid = True
for turn in range(data['numTurns']):
    #print turn
    #print droneCommandId
    #print droneStates
    for droneId in range(data['numDrones']):

        if droneStates[droneId]['wait'] == 0:
            if len(data_commands['commands'][droneId]) > droneCommandId[droneId]:
                nextCommand = data_commands['commands'][droneId][droneCommandId[droneId]]
                #print nextCommand
                #print droneStates[droneId]
                if nextCommand['type'] == 'L':

                    whId = nextCommand['warehouse']
                    whX = data['warehousesData'][whId]['x']
                    whY = data['warehousesData'][whId]['y']
                    dX = droneStates[droneId]['x']
                    dY = droneStates[droneId]['y']
                    if dX == whX and dY == whY:
                        pNum = nextCommand['number']
                        pId = nextCommand['product']
                        whPnum = data['warehousesData'][whId]['items'][pId]

                        if whPnum >= pNum:
                            addPayload = pNum * data['productWeights'][pId]
                            if addPayload + droneStates[droneId]['payload'] <= data['maxPayload']:
                                data['warehousesData'][whId]['items'][pId] -= pNum
                                droneStates[droneId]['items'][pId] += pNum
                                droneStates[droneId]['payload'] += addPayload
                                droneCommandId[droneId] += 1
                                validMoves.append(getCommandString(nextCommand, droneId))
                            else:
                                doInvalid('payload too high', droneId=droneId)
                                #invalid
                        else:
                            # invalid
                            doInvalid('not enough in stock', droneId=droneId)
                    else:
                        dist = int(math.ceil(math.sqrt((whX-dX)**2+(whY-dY)**2)))
                        if dist - 1 + turn < data['numTurns']:
                            droneStates[droneId]['wait'] = dist - 1
                            #droneCommandId[droneId] += 1
                            #validMoves.append(getCommandString(nextCommand, droneId))
                            droneStates[droneId]['x'] = whX
                            droneStates[droneId]['y'] = whY
                        else:
                            doInvalid('exceed turn count', droneId=droneId)
                if nextCommand['type'] == 'U':
                    whId = nextCommand['warehouse']
                    whX = data['warehousesData'][whId]['x']
                    whY = data['warehousesData'][whId]['y']
                    dX = droneStates[droneId]['x']
                    dY = droneStates[droneId]['y']
                    if dX == whX and dY == whY:
                        pNum = nextCommand['number']
                        pId = nextCommand['product']
                        whPnum = data['warehousesData'][whId]['items'][pId]
                        dPnum = droneStates[droneId]['items'][pId]
                        if dPnum >= pNum:
                            data['warehousesData'][whId]['items'][pId] += pNum
                            addPayload = pNum * data['productWeights'][pId]
                            droneStates[droneId]['items'][pId] -= pNum
                            droneStates[droneId]['payload'] -= addPayload
                            droneCommandId[droneId] += 1
                            validMoves.append(getCommandString(nextCommand, droneId))
                        else:
                            # invalid
                            doInvalid('not enough in drone', droneId=droneId)
                    else:
                        dist = int(math.ceil(math.sqrt((whX-dX)**2+(whY-dY)**2)))
                        if dist - 1 + turn < data['numTurns']:
                            droneStates[droneId]['wait'] = dist - 1
                            #droneCommandId[droneId] += 1
                            #validMoves.append(getCommandString(nextCommand, droneId))
                            droneStates[droneId]['x'] = whX
                            droneStates[droneId]['y'] = whY
                        else:
                            doInvalid('turn count exceeded', droneId=droneId)

                if nextCommand['type'] == 'W':

                    if nextCommand['turns'] - 1 + turn < data['numTurns']:
                        droneStates[droneId]['wait'] = nextCommand['turns'] - 1
                        droneCommandId[droneId] += 1
                        validMoves.append(getCommandString(nextCommand, droneId))
                    else:
                        doInvalid('turncount exceeded', droneId=droneId)
                if nextCommand['type'] == 'D':
                    #rint nextCommand
                    #print data['orderData']
                    oId = nextCommand['order']
                    oX = data['orderData'][oId]['x']
                    oY = data['orderData'][oId]['y']
                    dX = droneStates[droneId]['x']
                    dY = droneStates[droneId]['y']
                    if dX == oX and dY == oY:
                        pNum = nextCommand['number']
                        pId = nextCommand['product']

                        dPnum = droneStates[droneId]['items'][pId]
                        if dPnum >= pNum:
                            data['orderData'][oId]['itemsList'][pId] -= pNum
                            addPayload = pNum * data['productWeights'][pId]
                            droneStates[droneId]['items'][pId] -= pNum
                            droneStates[droneId]['payload'] -= addPayload
                            droneCommandId[droneId] += 1
                            if np.sum(data['orderData'][oId]['itemsList']) == 0:
                                score += (data['numTurns']-float(turn))/data['numTurns']*100.
                                #score
                                validMoves.append(getCommandString(nextCommand, droneId))
                                #print 'delivered'
                                #print score
                            elif np.sum(data['orderData'][oId]['itemsList']) < 0:
                                doInvalid('negative order list', droneId=droneId)
                                #invalid
                        else:
                            # invalid
                            doInvalid('not enough loaded in drone', droneId=droneId)
                        #print data['orderData']
                    else:
                        dist = int(math.ceil(math.sqrt((oX-dX)**2+(oY-dY)**2)))

                        if dist - 1 + turn < data['numTurns']:
                            droneStates[droneId]['wait'] = dist - 1
                            #droneCommandId[droneId] += 1
                            #validMoves.append(getCommandString(nextCommand, droneId))
                            droneStates[droneId]['x'] = oX
                            droneStates[droneId]['y'] = oY
                        else:
                            doInvalid('turncount exceeded', droneId=droneId)
        else:
            droneStates[droneId]['wait'] -= 1

print score
with open('outfile.out', 'wb') as outFile:
    for string in validMoves:
        #print >>outFile, string
        print string
