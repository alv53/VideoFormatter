import sys, os, re, datetime


def AddLeadingChars(value, maxLen, leadingChar):
	returnVal = value
	while len(returnVal) < maxLen:
		returnVal = leadingChar + returnVal 
	return returnVal

def GetNewNames(files):
	newNames = list()
	episodeNumbers = list()
	numDigits = 0

	for i in range(len(files)):
		newName = files[i]
		
		# Get episode number
		episodeStart = newName.find(name) + len(name) + 1
		newName = newName[episodeStart:]
		search = re.search("\d", newName)
		if not search:
			print "Error parsing episode number"
			sys.exit()
		start = newName[search.start():]
		search = re.search("\D", start)
		episodeNumber = start[:search.start()]
		# Remove prepending 0s for calculating number of digits
		while episodeNumber[0] == '0':
			episodeNumber = episodeNumber[1:]
		episodeNumbers.append(episodeNumber)	
		if len(str(episodeNumber)) > numDigits:
			numDigits = len(str(episodeNumber))
			
	for i in range(len(files)):
		newName = files[i]

		# Get file extension
		stringList = newName.split('.')
		ext = stringList[len(stringList) - 1]
		ext = '.' + ext

		appended = ""
		# Add resolution
		if "720" in newName:
			appended = " [720p]" 
		if "1080" in newName:
			appended = " [1080p]"
		if "480" in newName:
			appended = " [480p]"

		newName = newName.replace('-', ' ')
		newName = newName.replace('_', ' ')
		newName = newName.replace('.', ' ')
		
		while "  " in newName:
			newName = newName.replace("  "," ")

		# Add Leading 0s so all episode numbers have the same length
		episodeNumbers[i] = AddLeadingChars(episodeNumbers[i],numDigits,"0")

		# Combine the name, the number, and the extension
		newName = name + " - " + episodeNumbers[i] + appended + ext

		episodeNumbers.append(episodeNumber)
		# Add to our list of new names
		newNames.append(newName)
	return newNames

# Ending format will be [AnimeName] - [Episode #] [Resolution if applicable].extension
# Make sure we have the correct format for the command line arguments
if len(sys.argv) != 2:
	print "Usage: python " + os.path.basename(__file__) + " [directory with files]"
	sys.exit()
currDir = os.getcwd()
os.chdir(os.path.expanduser("~/Shared/AnimeFormatter"))

log = open("log.txt", 'a+')

os.chdir(currDir)
# get to directory
dirToRename = sys.argv[1]
os.chdir(dirToRename)
allFiles = os.listdir('.')
print "\nAll files in %s"%(dirToRename)
for File in allFiles:
	print File
# Get extension(s) from user
extension = "mkv mp4 m2ts avi"
extensions = extension.split(' ')
for ext in extensions:
	if not ext.startswith('.'):
		ext = '.' + ext

# Get files ending in the appropriate extension(s)
files = list()
for curr in allFiles:
	for ext in extensions:
		if curr.endswith(ext):
			files.append(curr)

print "\nFiles with the extension(s): " + extension
responded = False
while not responded:
	# Print the files
	print "\nFiles in: " + dirToRename
	for i in range(len(files)):
		print "%d) %s"%(i, files[i])
	print "\nExclude any of the above?(List numbers, 'n' or '' for all ok)"
	response = raw_input()
	if response == 'n' or response == '':
		responded = True
	else:
		ExcludeListInds = response.split(' ')
		ExcludeList = [files[int(ind)] for ind in ExcludeListInds]
		files = [f for f in files if f not in ExcludeList]
		
# Get names to use when parsing
dirList = os.getcwd().split('/')
name = dirList[len(dirList) - 1]

# Save old names
OldNames = list()
for i in range(len(files)):
	OldNames.append(files[i])

# Get new names
newNames = GetNewNames(files)

# Check with user before altering files
templog = ""
responded = False

# We do alter files, but not undo the changes after getting the new names
while not responded:
	# reset log line in case we do not like these changes
	templog = ""
	for i in range(len(files)):
		if not files[i] == newNames[i]:
			line = ("%d) " + files[i] + " ---> " + newNames[i]) % i 
			print line
			templog += line + "\n"
	print "\nAre these new file names acceptable? (y - yes/n - no/file #s to alter). Unchanged lines will not appear."
	response = raw_input()
	if (response == 'y' or response =='n'):
		responded = True
	elif response != "":
		# Get new names manually
		ManList = response.split(' ')
		TempNames = list()
		for ToChange in ManList:
			print "\nEnter new name for %d) %s ---> %s" % (int(ToChange), OldNames[int(ToChange)], newNames[int(ToChange)])
			print "Default will be unchanged\n"
			Result = raw_input()
			if not Result == "":
				TempNames.append(Result)

		# Hide the ones we are manually changing before updating names. This makes sure the episode numbers are set correctly.
		files.pop(int(ToChange))
		newNames = GetNewNames(files)

		# Insert the manually changed values to newNames and back to files
		for ToChange in ManList:
			newNames.insert(int(ToChange), TempNames.pop(0))
		files.insert(int(ToChange), OldNames[int(ToChange)])

if response == 'n':
	print "\nOk, bye!"
	sys.exit()

if not templog == "":	
	time = datetime.datetime.now()
	dateStamp = AddLeadingChars(str(time.month),2,"0") + "-" + AddLeadingChars(str(time.day),2,"0") + "-" + str(time.year)
	timeStamp = AddLeadingChars(str(time.hour),2,"0") + ":" + AddLeadingChars(str(time.minute),2,"0")
	if dirToRename.endswith('/'):
		dirToRename = dirToRename[:len(dirToRename)-1]
	templog =  "Formatting " + dirToRename + " - " + dateStamp + " " + timeStamp + "\n" + templog
	log.write(templog + "\n")
log.close()
print "\nRenaming files..."
for i in range(len(files)):
	os.rename(files[i], newNames[i])

