import sys, os

def main(args):
	lpfile = args[1]
	scheduleFile = args[2]
	with open(scheduleFile, 'r') as s:
		schedule = eval(s.read())
	
	with open(lpfile, 'r') as f:
		lpDATA = f.read()
	
	if(schedule is None or lpDATA is None):
		print("fails")
		quit()
	
	for i in range(0,24):
		time = 'time'+str(i)+'_Cost'
		print(time +" "+str(schedule[i]))
		lpDATA = lpDATA.replace(time, str(schedule[i]))

	newFilename = scheduleFile.split(".")[0] + "_" + lpfile
	
	with open(newFilename, 'w') as n:
		n.write(lpDATA)

if __name__ == '__main__':
	main(sys.argv)