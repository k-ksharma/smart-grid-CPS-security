def main():
	dict = { 
		"user1_task1":(20,23,1,1),
		"user1_task2":(18,23,1,2),
		"user1_task3":(19,21,1,1),
		"user1_task4":(12,20,1,3),
		"user1_task5":(6,12,1,3),
		"user1_task6":(18,20,1,2),
		"user1_task7":(4,10,1,2),
		"user1_task8":(12,18,1,2),
		"user1_task9":(7,14,1,3),
		"user1_task10":(8,14,1,3),
		"user2_task1":(11,22,1,2),
		"user2_task2":(5,11,1,2),
		"user2_task3":(5,23,1,1),
		"user2_task4":(6,20,1,3),
		"user2_task5":(19,19,1,1),
		"user2_task6":(18,21,1,2),
		"user2_task7":(3,23,1,3),
		"user2_task8":(21,23,1,2),
		"user2_task9":(13,17,1,1),
		"user2_task10":(6,11,1,2),
		"user3_task1":(20,23,1,2),
		"user3_task2":(15,21,1,3),
		"user3_task3":(11,15,1,2),
		"user3_task4":(2,17,1,3),
		"user3_task5":(13,16,1,2),
		"user3_task6":(10,18,1,2),
		"user3_task7":(21,23,1,2),
		"user3_task8":(20,23,1,1),
		"user3_task9":(7,21,1,2),
		"user3_task10":(0,7,1,3),
		"user4_task1":(1,8,1,1),
		"user4_task2":(11,20,1,2),
		"user4_task3":(12,19,1,3),
		"user4_task4":(11,16,1,3),
		"user4_task5":(16,18,1,1),
		"user4_task6":(19,23,1,3),
		"user4_task7":(22,23,1,1),
		"user4_task8":(12,19,1,2),
		"user4_task9":(8,20,1,2),
		"user4_task10":(4,12,1,2),
		"user5_task1":(4,20,1,1),
		"user5_task2":(18,22,1,3),
		"user5_task3":(4,16,1,1),
		"user5_task4":(2,16,1,3),
		"user5_task5":(16,23,1,2),
		"user5_task6":(6,18,1,2),
		"user5_task7":(2,6,1,1),
		"user5_task8":(13,17,1,3),
		"user5_task9":(15,23,1,1),
		"user5_task10":(17,23,1,1)}
	
	
	f = open("lpHelperFile.txt", mode='w', encoding='utf-8')
	for i in range(0,24):
		tasks = [x for x in dict.keys() if int(dict[x][0])<=i and i<=int(dict[x][1]) and 'user1' in x]
		if(len(tasks)>0):
			out = ""
			out = "time"+str(i)+"_Load="
			for j in range(0,len(tasks)-1):
				out = out + str(tasks[j]) +"_" +str(i) + "+"
			out = out + str(tasks[-1]) +"_" +str(i) + ";\n"
			f.write(out)
	
	f.write("\n")
	for k,v in dict.items():
		for i in range(int(v[0]),int(v[1])+1):
			f.write("0<="+str(k)+"_"+str(i)+"<=1;\n")
		out = ""
		for i in range(int(v[0]),int(v[1])):
			out = out + str(k)+"_"+str(i)+"+"
		out = out + str(k)+"_"+str(int(v[1]))+"="+str(v[3])+";\n"
		f.write(out)
		f.write("\n\n")
	f.close()

if __name__ == '__main__':
	main()