import sys
from collections import OrderedDict
from operator import itemgetter

def printSolution(exploredStates, algo):
	outputFile = open("output.txt","w")
	key = exploredStates.keys()[-1]
	solution = OrderedDict()
	while not (key == "NULL"):
		if algo == "BFS" or algo == "DFS":
			solution[key] = exploredStates[key][1]
		elif algo == "UCS":
			solution[key] = exploredStates[key][0]
		elif algo == "A*":
			solution[key] = exploredStates[key][3]
		key = exploredStates[key][2]
	
	for key in reversed(solution.keys()):
		outputFile.write(key + " " + str(solution[key]) + "\n")
	outputFile.close()

def executeAlgo(algo,startState,goalState,noOfLiveTraffic,liveTraffic,noOfSundayTraffic,sundayTraffic):
	openStates = OrderedDict()
	exploredStates = OrderedDict()
	openStates.setdefault(startState,[0]*4)
	openStates[startState][0] = int(0) #COST (g(n) for UCS and f(n) for A*)
	openStates[startState][1] = int(0) #DEPTH (for BFS and DFS)
	openStates[startState][2] = "NULL" #PARENT
	openStates[startState][3] = int(0) #PATHCOST_BACKUP (g(n) for A*)

	if algo == "A*":
		openStates[startState][0] = int(sundayTraffic[startState])
	while True:
		if not openStates:
			return failure
		currnode = openStates.keys()[0] #Always extract first element
		if currnode == goalState:
			exploredStates[currnode] = openStates[currnode]
			openStates.pop(currnode,None)
			printSolution(exploredStates, algo)
			return currnode
		children = OrderedDict()

		if algo == "BFS":
			if currnode in liveTraffic:
				for key in liveTraffic[currnode].keys():
					children.setdefault(key, [0]*4)
					children[key][0] = int(0)
					children[key][1] = int(openStates[currnode][1]) + 1
					children[key][2] = currnode
					children[key][3] = int(0)
			while children:
				child = children.keys()[0]
				if child not in openStates.keys() and child not in exploredStates.keys():
					openStates[child] = children[child]
				children.pop(child,None)
			exploredStates.setdefault(currnode,[0]*4)
			exploredStates[currnode] = openStates[currnode]
			openStates.pop(currnode,None)

		elif algo == "DFS":
			frontier = OrderedDict()
			if currnode in liveTraffic:
				for key in liveTraffic[currnode].keys():
					children.setdefault(key, [0]*4)
					children[key][0] = int(0)
					children[key][1] = int(openStates[currnode][1]) + 1
					children[key][2] = currnode
					children[key][3] = int(0)
			while children:
				child = children.keys()[0]
				if child not in openStates.keys() and child not in exploredStates.keys():
					frontier[child] = children[child]
				# if child in exploredStates.keys() :
				# 	frontier[child] = children[child]
				# As per hint : don't update if already exists in openStates
				# if child in openStates.keys():
				# 	frontier[child] = children[child]
				# 	openStates[child] = children[child]
				children.pop(child,None)

			if frontier:
				openStates = OrderedDict(list(frontier.items()) + list(openStates.items()))
			exploredStates.setdefault(currnode,[0]*4)
			exploredStates[currnode] = openStates[currnode]
			openStates.pop(currnode,None)

		elif algo == "UCS":
			if currnode in liveTraffic:
				for key in liveTraffic[currnode].keys():
					children.setdefault(key, [0]*4)
					children[key][0] = int(openStates[currnode][0]) + int(liveTraffic[currnode][key])
					children[key][1] = int(openStates[currnode][1]) + 1
					children[key][2] = currnode
					children[key][3] = int(0)
			while children:
				child = children.keys()[0]
				if child not in openStates.keys() and child not in exploredStates.keys():
					openStates[child] = children[child]
				elif child in openStates.keys():
					if children[child][0] < openStates[child][0]:
						openStates.pop(child,None)
						openStates[child] = children[child]
				elif child in exploredStates.keys():
					if children[child][0] < exploredStates[child][0]:
						exploredStates.pop(child,None)
						openStates[child] = children[child]
				children.pop(child,None)
			exploredStates.setdefault(currnode,[0]*4)
			exploredStates[currnode] = openStates[currnode]
			openStates.pop(currnode,None)
			openStates = OrderedDict(sorted(openStates.items(), key=itemgetter(1)))

		elif algo == "A*":
			if currnode in liveTraffic:
				for key in liveTraffic[currnode].keys():
					children.setdefault(key, [0]*4)
					children[key][0] = int(openStates[currnode][3]) + int(liveTraffic[currnode][key]) + int(sundayTraffic[key]) # f(n) = g(n) + h(n)
					children[key][1] = int(openStates[currnode][1]) + 1
					children[key][2] = currnode
					children[key][3] = int(openStates[currnode][3]) + int(liveTraffic[currnode][key]) #Backup g(n)
			while children:
				child = children.keys()[0]
				if child not in openStates.keys() and child not in exploredStates.keys():
					openStates[child] = children[child]
				elif child in openStates.keys():
					if children[child][0] < openStates[child][0]:
						openStates.pop(child,None)
						openStates[child] = children[child]
				elif child in exploredStates.keys():
					if children[child][0] < exploredStates[child][0]:
						exploredStates.pop(child,None)
						openStates[child] = children[child]
				children.pop(child,None)
			exploredStates.setdefault(currnode,[0]*4)
			exploredStates[currnode] = openStates[currnode]
			openStates.pop(currnode,None)
			openStates = OrderedDict(sorted(openStates.items(), key=itemgetter(1)))

if __name__ == "__main__":

	inputFile = open("input.txt","r")
	
	algo = ""
	startState = ""
	goalState = ""
	noOfLiveTraffic = 0
	liveTraffic = OrderedDict()
	noOfSundayTraffic = 0
	sundayTraffic = OrderedDict()
	for lineNo,line in enumerate(inputFile):
		if lineNo == 0:
			algo = line.strip()
		elif lineNo == 1:
			startState = line.strip()
		elif lineNo == 2:
			goalState = line.strip()
		elif lineNo == 3:
			noOfLiveTraffic = line.strip()
		elif lineNo > 3 and lineNo <= 3 + int(noOfLiveTraffic):
			values = line.strip().split()
			src = values[0]
			dest = values[1]
			pathCost = values[2]
			liveTraffic.setdefault(src, OrderedDict())
			liveTraffic[src][dest] = pathCost 
		elif lineNo == 3 + int(noOfLiveTraffic) + 1:
			noOfSundayTraffic = line.strip()
		elif lineNo <= 3 + int(noOfLiveTraffic) + 1 + int(noOfSundayTraffic):
			values = line.strip().split()
			state = values[0]
			heuristicCost = values[1]
			sundayTraffic[state] = heuristicCost

	executeAlgo(algo,startState,goalState,noOfLiveTraffic,liveTraffic,noOfSundayTraffic,sundayTraffic)
	inputFile.close()
