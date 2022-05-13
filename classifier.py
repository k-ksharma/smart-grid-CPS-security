from collections import Counter
import sys, os, math
import numpy as np


PETHOLD = 5 ##suspicions threshold
OHHOLD = 53 ##confidence threshold

#getters
def getPETHOLD():
	global PETHOLD
	return PETHOLD

#setters
def setPETHOLD(value=5):
	global PETHOLD
	PETHOLD = value

#getters
def getOHHOLD():
	global OHHOLD
	return OHHOLD

#setters
def setOHHOLD(value=50):
	global OHHOLD
	OHHOLD = value


#parsing filename
def _parseFile(fileName):
	if(os.path.splitext(fileName)[1] != ".txt"): return
	data = []
	with open(fileName, mode='r', encoding='utf-8') as f:
		for line in f:
			vec = _parseLine(line)
			if(len(vec)>=24):
				data.append(vec)
	return data

def _parseLine(line):
	if(line == "" or line == " "): return []
	v = list(line.split(","))
	if(len(v) == 24 or len(v) == 25): return v

def _chooseK(data):
	k = math.floor(math.sqrt(len(data)))
	if(k%2==0): k+=1
	return k


'''
Input will be test vector, training data, k from _chooseK function
Output will be prediction and confidence
'''
def _knn(test, data, k):
	#init
	neighbours = []
	kDistPack = []
	
	#for all traing vectors
	for d in data:
		dist = _distance(test,d)
		#getting the k smallest neighbour

		neighbours = _kSmallestSoFar(dist, d, neighbours, k)
		
	for n in neighbours:
		kDistPack.append(n[1][0])
	
	#count of frequent appearence
	count = Counter(kDistPack).most_common(k)

	if(len(count) == 1): return count[0][0], 1
	#calculating confidence and percentage
	confidence = int((count[0][1] / (count[0][1] + count[1][1]))*100)
	#returns most common item and the first result and confidence
	return count[0][0], confidence

# euclidean distance calculation for vectors
def _distance(v1,v2):
	sum = float(0.0)
	for i in range(0,23):
		sum += math.pow( float(v1[i]) - float(v2[i]) , 2 )
	return math.sqrt(sum)

#getting k nearest neighbours so far
def _kSmallestSoFar(dist: float, point, neighbours: [[float,str]], k: int) ->[[float,str]]:
	if(len(neighbours) < min(10,k)) :
		neighbours.append([ dist , point[-1]])
		#always keeping a sorted list
		neighbours.sort()
		return neighbours
	if(dist > neighbours[-1][0]): return neighbours
	
	neighbours.append([ dist , point[-1]])
	#keping a list of sorted neighbours
	neighbours.sort()
	
	return neighbours[:k]


#testing the accuracy of knn
def _accuracy_knn(training, k, outputFile=None):
	f = None
	if(not outputFile is None):
		f = open(outputFile, 'w')
	step = math.floor(len(training) / 10.0)
	correct = 0
	totalPercent = 0.0
	
	for i in range(0,len(training)):
		if(i % step == 0):
			print(str(i))
		testElement = training[i]
		modifiedTraining = training[:i] + training[i+1:]
		prediction, confidence = courseClassifier(testElement, modifiedTraining, k)
		if(int(prediction) == int(testElement[-1])):
			correct = correct + 1
			totalPercent = totalPercent + confidence
		del(prediction)
		del(confidence)
		del(testElement)
		del(modifiedTraining)
	
	#loop number and how many so far correct and number in traing data
	line = str(i+1) + ": " + str(correct) +" out of "+ str(len(training)) + " correct, at " + str((totalPercent/(i+1)))+"% total confidence"
	print(line)
	if(not f is None):
		f.write(line+'\n')
		f.close()
	return correct,(totalPercent/len(training))*100

#detecting misses by KNN
def _suspicion(festFectVector, data, k):
	#setting suspicions baselines
	high, mid, low, sus = 5,2,1,0
	#checking if high suspicion
	if((len(festFectVector) !=24) and (len(festFectVector) !=25)): sus = sus + high
	PAR = np.sum([float(x) for x in festFectVector[0:23]])/24.0
	if(PAR >4.762): sus = sus + high
	for i in range(0,24):
		if(i ==25 and not int(festFectVector[i])==0 and not int(festFectVector[i])==1): sus = sus + high
		if(float(festFectVector[i]) <=0.0 and not i==25): sus = sus + high
		if(float(festFectVector[i]) > 7.0): sus = sus + low
		if(float(festFectVector[i]) > 8.0): sus = sus + mid
		if(float(festFectVector[i]) > 10.0): sus = sus + high
	if(len(data) < 9999): sus = sus + mid
	if(len(data) < 5000): sus = sus + high
	if(k <=0): sus = sus + high
	return sus

# Classifying a new festFectVector
def courseClassifier(festFectVector, data, k):
	#running knn
	prediction, confidence = _knn(festFectVector, data, k)
	
	#ignore if confidence is below threshold
	if(int(prediction) == 1 and int(confidence) <= getOHHOLD()):
		prediction = 0
		
	#getting the value of suspicion
	sus = _suspicion(festFectVector, data, k)
	#if suspicion > threshold
	if(sus >= getPETHOLD()):
		#labeling data as abnormal
		return 1, confidence + math.floor((100-confidence) /3)
	return prediction, confidence

#FN gets maxium value for energy from test data
def _getMax(training):
	max = 0.0
	for i in range(0,len(training)):
		for j in range(0,len(training[i])):
			if(float(training[i][j]) > float(max)): max = training[i][j]
	return max

#for all testing data, courseClassifier data, label as 0 or 1
def _categorize(testing, training, k, outputFile=None):
	labeled = []
	i = 1
	for t in testing:
		prediction, confidence = courseClassifier(t, training, k)
		labeled.append(('line'+str(i), prediction, str(confidence)+'%',t))
		line = "line "+str(i)+" = "+ str(prediction) +" @ "+ str(confidence) +'%'
		print(line)
		i = i +1
	
	if(not outputFile is None):
		f = open(outputFile, 'w')
		for t in [l for l in labeled]:
			for p in t[-1]:
				f.write(str(float(p))+',')
			f.write(str(int(t[1]))+'\n')
		f.close()
	return labeled


def main(args):
	if(len(args)<=1):
		print("No args")
		exit(0)

	training = _parseFile(args[1])
	testing = _parseFile(args[2])
	
	if(training is None or training is [] or testing is None or testing is []):
		print("bad input")
		quit()

	k = _chooseK(training)
	
	var = 0
	try:
		var = args[3]
	except:
		pass
	
	setOHHOLD(53)
	
	if(type(var) is str and os.path.splitext(var)[-1] == ".txt"):
		labed = _categorize(testing, training, k, var)
		abnormal = [int(l[0][4:]) for l in labed if int(l[1]) == 1]
		print(str(len(abnormal))+" Abnormal results, on lines: "+str(abnormal))
		quit()

	var = int(var)
	if(var == 0):
		labed = _categorize(testing, training, k)
		abnormal = [int(l[0][4:]) for l in labed if int(l[1]) == 1]
		print(str(len(abnormal))+" Abnormal results, on lines: "+str(abnormal))
	elif(var == 1):
		_accuracy_knn(training, k, "baseAccurace-KNN.txt")
	else:
		pass
		
	
if __name__ == '__main__':
	main(sys.argv)
	exit(0)