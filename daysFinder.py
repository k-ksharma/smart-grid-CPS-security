dayCount=0
tracker=[]
inputFile= open("TestingResults.txt", 'r')
while dayCount != 100:
	line=inputFile.readline()
	if int(line.split(",")[24])==1:
		tracker.append(dayCount+1)
	dayCount+=1

print(len(tracker),tracker,sep="\n")