# Example of kNN implemented from Scratch in Python

import csv
import random
import math
import operator



def getFilecolumns(filename) :
    filereader = csv.reader( open( filename ) )
    row_counter = 0
    column_header=[]
    for row in filereader :
        if row_counter == 0:
            row_header = row
            colnum = 0
            for col in row_header:
                column_header.append( row_header[colnum] )
                colnum += 1
        break
    return column_header

def loadDataSet( filename, split, trainingSet=[] , testSet=[] ) :
    column_header = getFilecolumns( filename )
    print column_header
    row_count = 0
    with open( filename, 'rb' ) as inputfile:
        lines = csv.reader(inputfile)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            print dataset[x]
            if ( row_count != 0 ) :
                for y in range(len(column_header)-1):
                    dataset[x][y] = float(dataset[x][y])
                if random.random() < split:
                    trainingSet.append(dataset[x])
                else:
                    testSet.append(dataset[x])
            row_count += 1

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataSet('data/glass.data', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')

main()
