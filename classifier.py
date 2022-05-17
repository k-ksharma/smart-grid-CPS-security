import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

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
''''

##loop to find the n-neighbours value - 
plt.rcParams["figure.figsize"] = (20,10)
train_accuracy = []
test_accuracy = []
n_neighbors = range(1, 15)

for n in n_neighbors :
    knn = KNeighborsClassifier(n_neighbors = n)
    knn.fit(xTrain, yTrain)
    train_accuracy.append(knn.score(xTrain, yTrain))
    test_accuracy.append(knn.score(xTest, yTest))
     
plt.plot(n_neighbors, train_accuracy, label = 'train_accuracy')
plt.plot(n_neighbors, test_accuracy, label = 'test_accuracy')
plt.xlabel("k", fontsize = 15)
plt.ylabel("accuracy", fontsize = 15)
plt.show()

##command to check the accuracy, once we have selected an optimal value of number of n neighbours

knn = KNeighborsClassifier(n_neighbors = 12)
knn.fit(xTrain, yTrain)
print("test accuracy of knn with k=",12," is ",metrics.accuracy_score(yTest,  knn.predict(xTest)))

'''

knn = KNeighborsClassifier(n_neighbors = 12)
knn.fit(xTrain, yTrain)
print("Accuracy of knn with k=",12," is ",metrics.accuracy_score(yTest,  knn.predict(xTest))*100, "%")

#predicting the values for the TestingResults from TesingData using TrainingData
energyPred=knn.predict(xClassify)
predDS = pd.DataFrame({'Prediction': energyPred})
testDS = testDS.join(predDS)
testDS.to_csv("TestingResults.txt", header=None, index=None)

print("Prediction of abnormal values are: ", energyPred)