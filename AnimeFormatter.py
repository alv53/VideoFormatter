import sys, os, re

# Ending format will be [AnimeName] [Episode #] [FileEnding]
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

# Get extension(s) from user
print "\nFile extension(s)? (default: mkv) (Seperate with a space if multiple)"
Extension = raw_input()
if Extension == "":
	Extension = "mkv"
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
	
print "\nCurrent Anime Name? (default: " + Name + ")"
ParsedName = raw_input()
if not ParsedName == "":
	if not ParsedName == Name:
		Response = ""
		while not (Response == 'y' or Response == 'n'):
			print "\nWould you like to rename the folder to: " + ParsedName + "? (y - yes/n - no)"
			Response = raw_input()
		if Response =='y':
			os.chdir("..")
			os.rename(Name, ParsedName)	
			os.chdir(ParsedName)
		Name = ParsedName

print "\nNew Anime Name? (default: " + Name + ")"
New = raw_input()
if New == "":
	New = Name
print "\n"

# NewNames will store all the new names, so the user can confirm before changing the file names
NewNames = list()
OldNames = list()
# Loop through all the files
for i in range(len(Files)):
	OldNames.append(Files[i])
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

	# I dislike leading 0s
	while EpisodeNum.startswith('0'):
		EpisodeNum = EpisodeNum[1:]

	# Combine the name, the number, and the extension
	NewName = New + " - " + EpisodeNum + Appended + Ext

	# Add to our list of new names
	NewNames.append(NewName)

	# Print it

# Check with user before altering files
templog = ""
Responded = False
while not Responded:
	templog = ""
	for i in range(len(Files)):
		line = ("%d) " + Files[i] + " ---> " + NewNames[i]) % i 
		print line
		templog += line + "\n"
	print "\nAre these new file names acceptable? (y - yes/n - no/s - some)"
	Response = raw_input()
	if (Response == 'y' or Response =='n'):
		Responded = True
	if Response == 's':
		print "\nWhich files do you not want to alter? Seperate the numbers with a space (1 4 20)"
		ManuallyChange = raw_input()
		# while ManuallyChange
		ManList = ManuallyChange.split(' ')
		for ToChange in ManList:
			print "\nEnter new name for %d) %s ---> %s" % (int(ToChange), OldNames[int(ToChange)], NewNames[int(ToChange)])
			print "Default will be unchanged\n"
			Result = raw_input()
			if not Result == "":
				NewNames[int(ToChange)] = Result


if Response == 'n':
	print "\nOk, bye!"
	sys.exit()

log.write(templog + "\n")
log.close()
print "\nRenaming files..."
# Rename all the files
# print len(Files)
# print len(NewNames)
for i in range(len(Files)):
	os.rename(Files[i], NewNames[i])

