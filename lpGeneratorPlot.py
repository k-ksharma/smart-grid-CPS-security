from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def readData():
    #feeding user task from excel file shared
    xlFile = pd.read_excel ('COMP3217CW2Input.xlsx', sheet_name = 'User & Task ID')
    taskName = xlFile['User & Task ID'].tolist()
    readyTime = xlFile['Ready Time'].tolist()
    deadline = xlFile['Deadline'].tolist()
    maxEnergyPerHour = xlFile['Maximum scheduled energy per hour'].tolist()
    energyDemand = xlFile['Energy Demand'].tolist()
    tasks = []
    taskNames = []
    
    for k in range (len(readyTime)):
        task = []
        task.append(readyTime[k])
        task.append(deadline[k])
        task.append(maxEnergyPerHour[k])
        task.append(energyDemand[k])
        taskNames.append(taskName[k])
        
        tasks.append(task)
              
    #feeding predicted results from TestingResults.txt
    testDS = pd.read_csv('TestingResults.txt', header=None)
    yLabels = testDS[24].tolist()
    testDS = testDS.drop(24, axis=1)
    xData = testDS.values.tolist()
    
    return tasks, taskNames, xData, yLabels

def createLPModel(tasks, taskNames):
    '''function for scheduling problem'''

    #required variables
    taskVars = []
    c = []
    eq = []
    
    #creating a minimization LP model  
    model = LpProblem(name="Scheduling-problem", sense=LpMinimize)
    
    #looping through the list of tasks
    for ind, task in enumerate(tasks):
        n = task[1] - task[0] + 1
        tempList = []
        #lopping between readyTime and deadline for ech tasks and creating variables with given constraints
        for i in range(task[0], task[1] + 1):
            x = LpVariable(name=taskNames[ind]+'_'+str(i), lowBound=0, upBound=task[2])
            tempList.append(x)
        taskVars.append(tempList)

    #function for price minimization and appending to the model
    for ind, task in enumerate(tasks):
        for var in taskVars[ind]:
            price = price_list[int(var.name.split('_')[2])]
            c.append(price * var)
    model += lpSum(c)
            
    #additional constraints for the model      
    for ind, task in enumerate(tasks):
        tempList = []
        for var in taskVars[ind]:
            tempList.append(var)
        eq.append(tempList)
        model += lpSum(tempList) == task[3]
    
    #feedin the model to caller for plotting
    return model

#Plotting the model against hourly usage in the community
def plot(model, count):
    hours = [str(x) for x in range(0, 24)]
    pos = np.arange(len(hours))
    users = ['user1', 'user2', 'user3', 'user4', 'user5']
    color_list = ['midnightblue','mediumvioletred','mediumturquoise','gold','linen']
    plot_list = []
    to_plot = []
    
    #plot list for usage
    for user in users:
        tempList = []
        for hour in hours:
            hour_list_temp = []
            task_count = 0
            for var in model.variables():
                if user == var.name.split('_')[0] and str(hour) == var.name.split('_')[2]:
                    task_count += 1
                    hour_list_temp.append(var.value())
            tempList.append(sum(hour_list_temp))
        plot_list.append(tempList)
    
    #stacked bar plot
    plt.bar(pos,plot_list[0],color=color_list[0],edgecolor='black',bottom=0)
    plt.bar(pos,plot_list[1],color=color_list[1],edgecolor='black',bottom=np.array(plot_list[0]))
    plt.bar(pos,plot_list[2],color=color_list[2],edgecolor='black',bottom=np.array(plot_list[0])+np.array(plot_list[1]))
    plt.bar(pos,plot_list[3],color=color_list[3],edgecolor='black',bottom=np.array(plot_list[0])+np.array(plot_list[1])+np.array(plot_list[2]))
    plt.bar(pos,plot_list[4],color=color_list[4],edgecolor='black',bottom=np.array(plot_list[0])+np.array(plot_list[1])+np.array(plot_list[2])+np.array(plot_list[3]))

    plt.xticks(pos, hours)
    plt.xlabel('Hour')
    plt.ylabel('Energy Usage (kW)')
    plt.title('Energy Usage Per Hour For All Users\nDay %i'%count)
    plt.legend(users,loc=0)
    ##plt.savefig('Graph/Abnormal/Abnormal'+str(count)+'.png') ## for Abnormal graph
    plt.savefig('Graph/Normal/Normal'+str(count)+'.png') ## for Normal graph

    plt.clf()

    return plot_list

tasks, taskNames, xData, yLabels = readData()

#scheduling and plotting abnormal dataset graphs
#can be altered to plot normal as well
for ind, price_list in enumerate(xData):
    #label can be changed for normal or abnormal dataset depeneing upon the need
    if yLabels[ind] == 0:
        #creating model to solve and as input to plot function
        model = createLPModel(tasks, taskNames)
        answer = model.solve()
        #print the model solution
        print(answer)
        #Plot the model
        plot(model,ind+1)

print("\n Abnormal plots can be found in the /Graph/Abnormal folder")
print("\n Normal plots can be found in the /Graph/Normal folder")