# Smart Grid CPS Security
This code is part of my personal coursework.
To run the code we need a TrainingData.txt and TestingData.txt as input files.
The syntax for executions is
python -m classifier TrainingData.txt TestingData.txt [0 or 1 or Filename]

To test the program against testing data set and print its output to the console. In order to save the output to a text file, use the below command
> python -m classifier TrainingData.txt TestingData.txt 0 > classifierResult.txt

To run KNN Accuracy using training dataset and gives the output in a file. Use the below syntax
> python -m classifier TrainingData.txt TestingData.txt TestingResults.txt

LP folder is  for Linear Programming and the supporting codes have been put in place. 
lpHelper.py file helps generate the equations needed for LPsolve corresponding to all the users and their task.
further lpGenerate helps to generate files for the abnormal cases and their costs involved.