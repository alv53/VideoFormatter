import sys, os

if len(sys.argv) != 2:
	print "Usage: python " + os.path.basename(__file__) + " [directory with files]"
	sys.exit()

# get to directory
TargetDirectory = sys.argv[1]
print "Formatting folders in %s"%(TargetDirectory)
os.chdir(TargetDirectory)
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]

for folder in folders:
	os.system("python ~/Shared/AnimeFormatter/AnimeFormatter.py \"%s\""%(folder))