import sys, os

# First move all the mkv files into the Ongoing Anime folder
home = os.path.expanduser("~/Desktop")
os.chdir(home)
AllItems = os.listdir(".")
Mkvs = []
for item in AllItems:
	if item.endswith(".mkv"):
		Mkvs.append(item)
for Mkv in Mkvs:
	os.rename(Mkv, "Ongoing Anime/" + Mkv)

# Now move the mkv files into their appropriate folders
os.chdir("Ongoing Anime")
AllItems = os.listdir(".")
Mkvs = []
for item in AllItems:
	if item.endswith(".mkv"):
		Mkvs.append(item)
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
for folder in folders:
	for Mkv in Mkvs:
		# print "%s vs %s" % (Mkv, folder)
		if folder in Mkv:
			print " %s -> %s" % (Mkv, folder)
			os.rename(Mkv, folder + "/" + Mkv)
