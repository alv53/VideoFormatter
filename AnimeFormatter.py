import sys, os, re
def deepcopy(A):
    rt = []
    for elem in A:
        if isinstance(elem,list):
            rt.append(deepcopy(elem))
        else:
            rt.append(elem)
    return rt

def GetNewNames(Files):
	NewNames = list()
	EpisodeNumbers = list()
	NumDigits = 0

	for i in range(len(Files)):
		NewName = Files[i]
		
		# Get episode number
		EpisodeStart = NewName.find(Name) + len(Name) + 1
		AfterName = NewName[EpisodeStart:]
		Search = re.search("\d", AfterName)
		if not Search:
			print "Error parsing episode number"
			sys.exit()
		Start = AfterName[Search.start():]
		Search = re.search("\D", Start)
		EpisodeNum = Start[:Search.start()]
		EpisodeNumbers.append(EpisodeNum)	
		if len(str(EpisodeNum)) > NumDigits:
			NumDigits = len(str(EpisodeNum))
			
	for i in range(len(Files)):
		NewName = Files[i]

		# Get file extension
		StringList = NewName.split('.')
		Ext = StringList[len(StringList) - 1]
		Ext = '.' + Ext

		Appended = ""
		# Add resolution
		if "720" in NewName:
			Appended = " [720p]" 
		if "1080" in NewName:
			Appended = " [1080p]"
		if "480" in NewName:
			Appended = " [480p]"

		NewName = NewName.replace('-', ' ')
		NewName = NewName.replace('_', ' ')
		NewName = NewName.replace('.', ' ')
		
		while "  " in NewName:
			NewName = NewName.replace("  "," ")

		# Add Leading 0s
		while len(str(EpisodeNumbers[i])) < NumDigits:
			EpisodeNumbers[i] = "0" + EpisodeNumbers[i]
		
		# Combine the name, the number, and the extension
		NewName = Name + " - " + EpisodeNumbers[i] + Appended + Ext
		EpisodeNumbers.append(EpisodeNum)
		# Add to our list of new names
		NewNames.append(NewName)
	return NewNames

# Ending format will be [AnimeName] - [Episode #] [Resolution if applicable].extension
# Make sure we have the correct format for the command line arguments
if len(sys.argv) != 2:
	print "Usage: python " + os.path.basename(__file__) + " [directory with files]"
	sys.exit()
currDir = os.getcwd()
os.chdir(os.path.expanduser("~/Shared/AnimeFormatter"))
log = open('log.txt', 'a')
os.chdir(currDir)
# get to directory
DirToRename = sys.argv[1]
os.chdir(DirToRename)
AllFiles = os.listdir('.')
print "\nAll Files in %s"%(DirToRename)
for File in AllFiles:
	print File
# Get extension(s) from user
Extension = "mkv mp4 m2ts avi"
Extensions = Extension.split(' ')
for Ext in Extensions:
	if not Ext.startswith('.'):
		Ext = '.' + Ext

# Get files ending in the appropriate extension(s)
Files = list()
for curr in AllFiles:
	for Ext in Extensions:
		if curr.endswith(Ext):
			Files.append(curr)

print "\nFiles with the extension(s): " + Extension
Responded = False
while not Responded:
	# Print the files
	print "\nFiles in: " + DirToRename
	for i in range(len(Files)):
		print "%d) %s"%(i, Files[i])
	print "\nExclude any of the above?(List numbers, 'n' or '' for all ok)"
	Response = raw_input()
	if Response == 'n' or Response == '':
		Responded = True
	else:
		ExcludeListInds = Response.split(' ')
		ExcludeList = [Files[int(ind)] for ind in ExcludeListInds]
		Files = [f for f in Files if f not in ExcludeList]
		
# Get names to use when parsing
DirList = os.getcwd().split('/')
Name = DirList[len(DirList) - 1]

# Save old names
OldNames = list()
for i in range(len(Files)):
	OldNames.append(Files[i])

# Get new names
NewNames = GetNewNames(Files)

# Check with user before altering files
templog = ""
Responded = False

# We do altar Files, but not undo the changes after getting the new names
while not Responded:
	# reset log line in case we do not like these changes
	templog = ""
	for i in range(len(Files)):
		line = ("%d) " + Files[i] + " ---> " + NewNames[i]) % i 
		print line
		templog += line + "\n"
	print "\nAre these new file names acceptable? (y - yes/n - no/file numbers to alter)"
	Response = raw_input()
	if (Response == 'y' or Response =='n'):
		Responded = True
	elif Response != "":
		# Get new names manually
		ManList = Response.split(' ')
		TempNames = list()
		for ToChange in ManList:
			print "\nEnter new name for %d) %s ---> %s" % (int(ToChange), OldNames[int(ToChange)], NewNames[int(ToChange)])
			print "Default will be unchanged\n"
			Result = raw_input()
			if not Result == "":
				TempNames.append(Result)

		# Hide the ones we are manually changing before updating names. This makes sure the episode numbers are set correctly.
		Files.pop(int(ToChange))
		NewNames = GetNewNames(Files)

		# Insert the manually changed values to NewNames and back to Files
		for ToChange in ManList:
			NewNames.insert(int(ToChange), TempNames.pop(0))
		Files.insert(int(ToChange), OldNames[int(ToChange)])

if Response == 'n':
	print "\nOk, bye!"
	sys.exit()

log.write(templog + "\n")
log.close()
print "\nRenaming files..."
for i in range(len(Files)):
	os.rename(Files[i], NewNames[i])

