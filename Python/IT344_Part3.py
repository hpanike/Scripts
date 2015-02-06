import subprocess
import os
import shutil

SOURCE='/home/hpanike/Pictures/IT344-Lab5/' #Hard coded source location
DEST='/home/python-tester/testing/' #Hard coded destination location

src_file = os.listdir(SOURCE) #Get an object will all the files
print "The source directory: " + SOURCE + " before" #Print SOURCE before
subprocess.call(['ls','-al',SOURCE])
print"\nThe dest directory: " + DEST + " before" #Print the DEST before
subprocess.call(['ls','-al',DEST])

for filename in src_file: #Loop over all the files
    full_file_name = os.path.join(SOURCE, filename) #Get the full name
    if (os.path.isfile(full_file_name)): #Make sure we are sure what this file is 
        shutil.copy2(full_file_name, DEST) #Use a copy2 to cp the file.  This is like cp -p

print "The source directory after" #Print SOURCE after
subprocess.call(['ls','-al','/home/hpanike/Pictures/IT344-Lab5'])
print"\nThe dest directory after" #Print DEST after
subprocess.call(['ls','-al','/home/python-tester/testing'])

