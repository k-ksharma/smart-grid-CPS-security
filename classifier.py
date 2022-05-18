import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import re

#writing to file
def writeToFile(predictedList):
    listOfAbnormalVal=yPred.tolist()
    fileVal=[]
    fHandler=open("TestingData.txt","r")
    resultFile=open("TestingResults.txt","a")
    for i in range(len(listOfAbnormalVal)):
        inputVal=fHandler.readline()
        inputVal=re.sub('\n','',inputVal)
        inputVal=inputVal.split(",")
        tmpVar=str(listOfAbnormalVal[i])
        inputVal.append(tmpVar)
        inputVal=",".join(inputVal)
        resultFile.write(inputVal)
        resultFile.write("\n")
        inputVal=""
        
    resultFile.close()
    fHandler.close()

#feeding training dataset
trainDS = pd.read_csv('TrainingData.txt', header=None)
y = trainDS[24].tolist()
trainDS = trainDS.drop(24, axis=1)
x = trainDS.values.tolist()

#storing input before splitting
x = np.array(x)
y = np.array(y)
xTrainFull = x
yTrainFull = y

#feeding test data
testDS = pd.read_csv('TestingData.txt', header=None)
xClassify = testDS.values.tolist()

#splitting training dataset for testing
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=1004)

#normalising by scaling between 0 and 1
scaler = MinMaxScaler()
xTrain = scaler.fit_transform(xTrain)
xTest = scaler.transform(xTest)
xClassify = scaler.transform(xClassify)
xTrainFull = scaler.transform(xTrainFull)

#Gaussian Naive Bayes Classifiers
gnb = GaussianNB()
gnb.fit(xTrain, yTrain)
print("Accuracy for GNB classifier on Training set: ",gnb.score(xTrainFull, yTrainFull))

#Predicting the values for testingData.txt
yPred=gnb.predict(xClassify)
writeToFile(yPred)
print("The output has been written in TestingResults.txt file.")

#converting the output from normal/abnormal to days/no. of line of input for plotting and referencing
dayCount=0
tracker=[]
inputFile= open("TestingResults.txt", 'r')
while dayCount != 100:
	line=inputFile.readline()
	if int(line.split(",")[24])==1:
		tracker.append(dayCount+1)
	dayCount+=1

print("Count of abnormal schduling values predicted = "+len(tracker),"And the days are "+tracker,sep="\n")