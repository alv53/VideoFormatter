#!/usr/bin/env python

import sys, os, re, datetime

# Adds leadingChar in front of value until its length is maxLen
# Called by GetNewNames, FormatDirectory
# value: The string to add characters to
# maxLen: The desired length of the end result
# leadingChar: The character to prepend to value
# Returns: the new string with leadining characters added.
def AddLeadingChars(value, maxLen, leadingChar):
    returnVal = value

    # Loop to add characters
    while len(returnVal) < maxLen:
        returnVal = leadingChar + returnVal
    return returnVal

# Checks if a list has duplicates
# Called by GetNewNames
# theList: the list to check for duplicates
# Returns true or false
def anyDup(theList):
    seen = set()
    for x in theList:
        if x in seen:
            return True
        seen.add(x)
    return False

# Used to get the new formatted names of the given files
# Called by FormatDirectory
# files: the list of all the files to get new names for
# name: the name of the video series, to be used when parsing the old file name to create the new name
# Returns: A list with the formatted names of the video files
def GetNewNames(files, name):
    # NewNames will store the new names to be used for formatting
    newNames = list()

    # The list of the episode numbers will keep track of episode numbers
    episodeNumbers = list()

    # numDigits is needed when determinining how many leading 0s to add with AddLeadingChars()
    numDigits = 0

    # Look through all the files to determine the episode numbers
    for i in range(len(files)):
        currName = files[i]

        # Get episode number
        episodeStart = currName.find(name) + len(name) + 1
        currName = currName[episodeStart:]
        search = re.search("\d", currName)
        if not search:
            print "Error parsing episode number"
            sys.exit()
        start = currName[search.start():]
        search = re.search("\D", start)
        episodeNumber = start[:search.start()]

        # Remove prepending 0s for calculating number of digits
        # Necessary in case EVERY file has leading 0s, as we only want them if we need them
        while episodeNumber[0] == '0':
            episodeNumber = episodeNumber[1:]
        episodeNumbers.append(episodeNumber)

        # Update numDigits if needed
        if len(str(episodeNumber)) > numDigits:
            numDigits = len(str(episodeNumber))

    # Now we loop through to determine the new file names
    for i in range(len(files)):
        newName = files[i]

        # Get file extension
        stringList = newName.split('.')
        ext = stringList[len(stringList) - 1]
        ext = '.' + ext

        # appended is the string that will be added after the episode number, before the extension
        appended = ""

        # Add resolution if needed
        if "720" in newName:
            appended = " [720p]"
        if "1080" in newName:
            appended = " [1080p]"
        if "480" in newName:
            appended = " [480p]"

        # Remove characters that mess up parsing and make the name look messy.
        newName = newName.replace('-', ' ')
        newName = newName.replace('_', ' ')
        newName = newName.replace('.', ' ')

        # Replace multiple spaces with one space
        while "  " in newName:
            newName = newName.replace("  "," ")

        # Add Leading 0s so all episode numbers have the same length
        episodeNumbers[i] = AddLeadingChars(episodeNumbers[i],numDigits,"0")

        # Combine the name, the number, and the extension
        newName = name + " - " + episodeNumbers[i] + appended + ext

        # Add to our list of new names
        newNames.append(newName)

    # Return the array of new names
    return newNames

# Gets the most recent log entries for a given directory
# Called by FormatUndo
# directory: The directory to parse the log file for
# log: the log file to use to undo changes
# Returns: the string containing the most recent log entries
def GetMostRecent(directory, log):
    currDir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
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

# Removes the given lines from the log file
# Called by FormatUndo
# linesArray: The array containing the lines we want to remove
# Returns: Nothing
def RemoveFromLog(linesArray):
    # Get all the files in the directory (we got to the correct directory in FormatUndo), and rename them to their original names
    allFiles = os.listdir('.')
    for lineToUndo in linesArray:
        if " ---> " in lineToUndo:
            oldName = lineToUndo[lineToUndo.index(" ") + 1:lineToUndo.index(" ---> ")]
            changedName = lineToUndo[lineToUndo.index(" ---> ") + 6:]
            for toChange in allFiles:
                if toChange == changedName:
                    os.rename(toChange, oldName)

    # Remove the lines from the log
    currDir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Copy all the files from the log into the new log, IF we should add it
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

# Formats the video files in the directory
# Ending format will be [VideoName] - [Episode #] [Resolution if applicable].extension
# Called by main, FormatSub
# dirToRename: The directory we are trying to rename
# Returns: Nothing
def FormatDirectory(dirToRename):
    # Save curr directory
    currDir = os.getcwd()

    # Open log from directory with file
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    log = open("log.txt", 'a+')

    # Go back to the directory with the files to change
    os.chdir(currDir)
    os.chdir(dirToRename)

    # Get all the files in the directory
    allFiles = os.listdir('.')
    print "\nAll files in %s"%(dirToRename)
    for File in allFiles:
        print File

    # Space delimited string with accepted video extensions
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

    # Ask user if all the listed files are acceptable to be formatted
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
    newNames = GetNewNames(files, name)

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
        if ((response == 'y' or response =='n')):
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

            newNames = GetNewNames(files, name)

            # Insert the manually changed values to newNames and back to files
            for ToChange in ManList:
                newNames.insert(int(ToChange), TempNames.pop(0))
                files.insert(int(ToChange), OldNames[int(ToChange)])
    if response == 'n':
        print "\nOk, bye!"
        sys.exit()
    if anyDup(newNames):
        print "Duplicates in list, exiting to prevent file overwriting"
        sys.exit()
    # If we have altered some files
    if not templog == "":
        time = datetime.datetime.now()
        dateStamp = AddLeadingChars(str(time.month),2,"0") + "-" + AddLeadingChars(str(time.day),2,"0") + "-" + str(time.year)
        timeStamp = AddLeadingChars(str(time.hour),2,"0") + ":" + AddLeadingChars(str(time.minute),2,"0")
        if dirToRename.endswith('/'):
            dirToRename = dirToRename[:len(dirToRename)-1]
        templog =  "Formatting " + dirToRename + " - " + dateStamp + " " + timeStamp + "\n" + templog
        log.write(templog + "\n")
    log.close()

    # rename the files
    print "\nRenaming files..."
    for i in range(len(files)):
        os.rename(files[i], newNames[i])

# Moves all the video files from the source directory to dest, then sorts them
# Sorts video files into existing sub folders in dest. Useful when you have many assorted video files in one folder and want to organize them
# Called by main
# source: The source directory with all the video files
# dest: The destination directory with the subfolders to sort into (If no subfolder, then the files will just be moved to dest)
# Returns: Nothing
def VideoMover(source, dest):
    # First move all the mkv files into the Ongoing Anime folder
    currDir = os.getcwd()
    os.chdir(source)
    AllItems = os.listdir(".")
    videos = []
    for item in AllItems:
        if item.endswith(".mkv") or item.endswith(".mp4") or item.endswith(".avi") or item.endswith(".m2ts"):
            videos.append(item)
    for video in videos:
        os.rename(video, dest + "/" + video)

    # Now move the mkv files into their appropriate folders
    os.chdir(currDir)
    os.chdir(dest)
    AllItems = os.listdir(".")

    # Only get the files ending in mkv, mp4, avi, or m2ts
    # TODO: change this to using the a global list (that way we can change accepted extensions easily across all functions)
    videos = []
    for item in AllItems:
        if item.endswith(".mkv") or item.endswith(".mp4") or item.endswith(".avi") or item.endswith(".m2ts"):
            videos.append(item)

    # Move the files into their respective folders if they exist
    folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
    for folder in folders:
        for video in videos:
            if folder in video:
                print " %s -> %s" % (video, folder)
                os.rename(video, folder + "/" + video)

# Will call FormatDirectory on all of the subdirectories of the given directory.
# Useful for formatting an entire directory with shows at once
# Called by main
# dirWithSubdirs: The directory with all the subdirectories that we want to call FormatDirectory on
# Returns: Nothing
def FormatSub(dirWithSubdirs):
    # get to directory
    print "Formatting folders in %s"%(dirWithSubdirs)
    os.chdir(dirWithSubdirs)

    # Get all the directories
    folders = [f for f in os.listdir('.') if not os.path.isfile(f)]

    # Format all of them
    for folder in folders:
        os.system(os.path.dirname(os.path.realpath(__file__)) + "/./VideoFormatter.py FD \"%s\""%(folder))

# Will undo the most recent changes for the directory, then remove that entry from the log
# Useful for when you have accidently changed a directory you did not mean to
# Called by main
# dirToUndo: The directory we want to undo changes for
# Returns: Nothing
def FormatUndo(dirToUndo):
    os.chdir(dirToUndo)

    # Remove that pesky training '/'
    if dirToUndo.endswith("/"):
        dirToUndo = dirToUndo[:len(dirToUndo)-1]

    # Get the most recent lines
    toUndo = GetMostRecent(dirToUndo, "log.txt")

    # Get the lines in an array
    toUndoArr = toUndo.split('\n')

    # Remove the changes undone from the log
    RemoveFromLog(toUndoArr)

# Prints the usage instructions for the program
# Called by main
# Returns: Nothing
def PrintUsage():
    print "Usage: python " + os.path.basename(__file__) + " [Command (FD, VM, FS, FU)]"
    print "FD = Format Directory: Formats the given directory"
    print "VM = Moves all videos from the given directory into a certain folder, and sorts them into their respective sub folders"
    print "FS = Format Subdirectories: Formats an entire directory's subdirectories using VF"
    print "FU = Format Undo: Undoes the most recent change recorded on the log for a given directory"

# The main function which is what is called when the script is run
# Called by YOU!
def main():
    # Need at least two arguments (one to call the program, and one to pick the function)
    if len(sys.argv) < 2:
        PrintUsage()
        sys.exit()

    # Calls FormatDirectory
    if (sys.argv[1] == "FD"):
        if len(sys.argv) != 3:
            print "Usage: ./" + os.path.basename(__file__) + " FD [directory with files]"
            sys.exit()
        FormatDirectory(sys.argv[2])

    # Calls VideoMover
    elif (sys.argv[1] == "VM"):
        if len(sys.argv) != 4:
            print "Usage: ./" + os.path.basename(__file__) + " VM [source directory] [destination directory]"
            sys.exit()
        VideoMover(sys.argv[2], sys.argv[3])

    # Calls FormatSub
    elif (sys.argv[1] == "FS"):
        if len(sys.argv) != 3:
            print "Usage: ./" + os.path.basename(__file__) + " FS [directory with subdirectories]"
            sys.exit()
        FormatSub(sys.argv[2])

    # Calls FormatUndo
    elif (sys.argv[1] == "FU"):
        if len(sys.argv) != 3:
            print "Usage: ./" + os.path.basename(__file__) + " FU [directory to undo]"
            sys.exit()
        FormatUndo(sys.argv[2])

    # If none of the previous statements have been fulfilled, print the usage instructions
    else:
        PrintUsage()
        sys.exit()

# Call main!
main()
