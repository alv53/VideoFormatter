import sys, os, re

# Ending format will be [AnimeName] [Episode #] [FileEnding]
# Make sure we have the correct format for the command line arguments
if len(sys.argv) != 2:
	print "Usage: python " + os.path.basename(__file__) + " [directory with files]"
	sys.exit()

DirToRename = sys.argv[1]
os.chdir(DirToRename)
AllFiles = os.listdir('.')
print "\nFiles in: " + DirToRename
for curr in AllFiles:
	print curr
print "\nFile extension(s)? (default: .mkv)"
Extension = raw_input()
if Extension == "":
	Extension = "mkv"
if not Extension.startswith('.'):
	Extension = '.' + Extension
print "\nCurrent Anime Name?"	
Name = raw_input()
print "\nNew Anime Name? (default: same as current)"
New = raw_input()
if New == "":
	New = Name
# print "Want the [720p] resolution tag there? Possible options include \"720p\" or \"1080p\" (default: no tag)"
# Resolution = raw_input()
# if not Resolution == "":
# 	HasRes = True

# Navigate to the appropriate directory

Files = list()

# Get files ending in the appropriate extension
for curr in AllFiles:
	if curr.endswith(Extension):
		Files.append(curr)

# Generate new names
NewNames = list()
for i in range(len(Files)):
	# Don't you just hate anime with '_' in the titles instead of spaces?
	NewName = Files[i]
	NewExtension = Extension
	BoxedRes = ""
	HasRes = False
	Options = ["[720p]", "[1080p]", "[h264 720p]", "(1280x720)", "(1280x720 h264)", "[1280x720][h264]", "[1280x720][x264]"]
	for option in Options:
		if option in NewName:
			Appended = option
			if "720" in option:
				Appended = "[720p]"
			NewExtension = Appended + NewExtension
			HasRes = True
			BoxedRes = option

	# Replace those pesky underscores and dashes
	NewName = NewName.replace('_',' ')
	NewName = NewName.replace('-',' ')
	
	# Remove everything before Name
	NewName = NewName[NewName.find(Name):]

	# Replace everything in between the resolution and the extension 
	if HasRes:
		NewName = NewName[:NewName.find(BoxedRes)] + NewExtension
	while "  " in NewName:
		NewName = NewName.replace("  "," ")

	# print NewName
	StringList = NewName.split()

	# Deals with stuff like Ep01, where the episode number is prepended with Ep, EP, or ep
	# Apply new name and removing leading 0
	if StringList[len(StringList) - 2].startswith("Ep") or StringList[len(StringList) - 2].startswith("EP") or StringList[len(StringList) - 2].startswith("ep"):
		StringList[len(StringList) - 2] = StringList[len(StringList) - 2][2:]
	if StringList[len(StringList) - 2].startswith('0'):
		StringList[len(StringList) - 2] = StringList[len(StringList) - 2][1:]
	if 'v' in StringList[len(StringList) - 2]:
		StringList[len(StringList) - 2] = StringList[len(StringList) - 2][:StringList[len(StringList) - 2].find('v')]

	# Apply the new extension in case the previous HasRes condition was not fulfilled
	if not HasRes:
		StringList[len(StringList) - 2] += NewExtension
		StringList = StringList[:len(StringList) - 1]

	# Rejoin the list
	NewName = " ".join(StringList)
	
	# Replace the old name with the new one specified
	NewName = NewName.replace(Name, New)

	# Add to our list of new names
	NewNames.append(NewName)

	# Print it
	print (Files[i] + " ---> " + NewNames[i])

# Check with user before altering files
Responded = False
while not Responded:
	print "\nAre these new file names acceptable? (y/n)"
	Response = raw_input()
	if (Response == 'y' or Response =='n'):
		Responded = True

if Response == 'n':
	print "\nOk, bye!"
	sys.exit()

print "\nRenaming files..."
# Rename all the files
for i in range(len(Files)):
	os.rename(Files[i], NewNames[i])

