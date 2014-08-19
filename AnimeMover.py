import sys, os

# First move all the mkv files into the Ongoing Anime folder
Desktop = os.path.expanduser("~/Desktop")
os.chdir(Desktop)
AllItems = os.listdir(".")
videos = []
for item in AllItems:
	if item.endswith(".mkv") or item.endswith(".mp4") or item.endswith(".avi") or item.endswith(".m2ts"):
		videos.append(item)
for video in videos:
	os.rename(video, "Ongoing Anime/" + video)

# Now move the mkv files into their appropriate folders
os.chdir("Ongoing Anime")
AllItems = os.listdir(".")
videos = []
for item in AllItems:
	if item.endswith(".mkv") or item.endswith(".mp4") or item.endswith(".avi") or item.endswith(".m2ts"):
		videos.append(item)
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
for folder in folders:
	for video in videos:
		# print "%s vs %s" % (video, folder)
		if folder in video:
			print " %s -> %s" % (video, folder)
			os.rename(video, folder + "/" + video)
