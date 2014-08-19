import sys, os

# Returns the string with the most recent 
def GetMostRecent(directory, log):
	currDir = os.getcwd()
	os.chdir(os.path.expanduser("~/Shared/AnimeFormatter"))
	currLog = ""
	dirFound = False

	# Find the most recent line
	for line in open(log).readlines():
		if not dirFound:
			if line.startswith("Formatting"):
				if directory in line:
					currLog = line
					dirFound = True
		else: # Directory has already been found, so we are loading in the log
			if line == "\n":
				dirFound = False
			else:	
				currLog = currLog + line
	if currLog == "":
		print "Directory not found"
	os.chdir(currDir)
	return currLog

def RemoveFromLog(linesArray):
	allFiles = os.listdir('.')
	for lineToUndo in linesArray:
		if " ---> " in lineToUndo:
			# print lineToUndo
			# print lineToUndo.index(" ")
			oldName = lineToUndo[lineToUndo.index(" ") + 1:lineToUndo.index(" ---> ")]
			changedName = lineToUndo[lineToUndo.index(" ---> ") + 6:]
			for toChange in allFiles:
				if toChange == changedName:
					os.rename(toChange, oldName)				
	currDir = os.getcwd()
	os.chdir(os.path.expanduser("~/Shared/AnimeFormatter"))
	currLog = ""
	addLine = True;
	lines = open("log.txt","r").readlines()
	f = open("log.txt", "w")
	for line in lines:
		if line == linesArray[0] + "\n":
			addLine = False
		if addLine:
			f.write(line)
		if line == "\n":
			addLine = True
	f.close()
	os.chdir(currDir)

if len(sys.argv) != 2:
	print "Usage: python " + os.path.basename(__file__) + " [directory with files]"
	sys.exit()

dirToUndo = sys.argv[1]
os.chdir(dirToUndo)
if dirToUndo.endswith("/"):
	dirToUndo = dirToUndo[:len(dirToUndo)-1]
toUndo = GetMostRecent(dirToUndo, "log.txt")
toUndoArr = toUndo.split('\n')

# Remove the changes undone from the log
RemoveFromLog(toUndoArr)