import os
import sys

print "Environ['USER']: ", os.environ['USER'] #Print the USER ENViroment Variable
print "PATH environ variable: ", os.environ["PATH"] #Print the PATH ENVironment Variable
print "Script Filename: ", os.path.basename(__file__) #Print the name of the file this command is being run in.
