# Smart Grid CPS Security
This code is part of my personal coursework.
To run the code we need a TrainingData.txt and TestingData.txt as input files.
The syntax for executions is
python -m classifier TrainingData.txt TestingData.txt [0 or 1 or Filename]

0 to test the program against testing data set and print its output to the console. In order to save the output to a text file, use the below command
> python -m classifier TrainingData.txt TestingData.txt 0 > classifierResult.txt

1 to run KNN Accuracy using training dataset and gives the output in a file. Use the below syntax
> python -m classifier TrainingData.txt TestingData.txt TestingResults.txt

