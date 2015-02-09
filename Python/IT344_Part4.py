#Check permissions

import os
import stat
import sys
import pwd
import grp
import smtplib
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from email import Encoders
from email.MIMEBase import MIMEBase

def group_readable(filepath): #Look to see if a file is group readable.
    st = os.stat(filepath) #Get the os stat for the file
    return bool(st.st_mode & stat.S_IRGRP) #Mask the grp read bit to see if it is true or false.

def group_writeable(filepath): #Look to see if a file is group writeable.
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IWGRP)#Mask for grp write

def group_executable(filepath): #Look to see if a file is group executable.
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IXGRP)#Mask for grp execute

def world_readable(filepath): #Look to see if a file is world readable.
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IROTH)#Mask for other/world read

def world_writeable(filepath): #Look to see if a file is world writeable.
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IWOTH)#Mask for other/world write - This is a bad bad bad idea

def world_executable(filepath):#Look to see if a file is world executable.
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IXOTH)#Mask for other/world execute - This is a bad bad bad idea 

def add_results(results, message): #Add a result to the results file.
    results.writelines(message)

def get_path(filename): #Get the absolute path of the filename.
    path = os.path.abspath(filename)
    return path

def get_owner(filename): #Get the owner of the file.
    stat = os.stat(filename)
    uid = stat.st_uid
    return pwd.getpwuid(uid)[0]

def get_group(filename): #Get the group of the file.
    stat = os.stat(filename)
    gid = stat.st_gid
    return grp.getgrgid(gid)[0]

    
def email_me(results): #Function to email results to an email address. 
    
    yes_cmd=["y","Y","yes","Yes"] #Array of possible yes inputs.
    to = raw_input("Please enter your email address: ") #Get the email address you want to send too.
    subject = raw_input("Please enter the email subject: ") #Get the email subject.
    choice = raw_input("Would you like to enter a message to go along with your results [y,n]: ") #See if the user wants to send a message body with the results file.
    if choice in yes_cmd:
        user_msg = raw_input("Please enter a message to go along with your results: ") #If the user does want to send a file then get the message body.
    else:
        user_msg = ""
        
    gmail_user = "hpanike@gmail.com"  #The user name used to create a TLS session with smtp.gmail.com
    gmail_pwd = "ufzijcxvfrbcmbzr" #App Specific password
    
    smtpserver = smtplib.SMTP("smtp.gmail.com",587) #The smtp server with port
    smtpserver.ehlo() #Introduce yourself
    smtpserver.starttls() #Start a TLS session
    smtpserver.ehlo() #Make sure you still good
    smtpserver.login(gmail_user, gmail_pwd) #Create the session with the provided user and password
    
    msg = MIMEMultipart() #Create a multipart message
    msg.preamble = "This is a multi-part message in MIME format. This email is created by Hayden Panike's Security Scanner Script.\n" #Preamble to the message - Check the header fields to see it show up.
    msg.epilogue = '' #No epiloge, though you can add one.
    
    body = MIMEMultipart('alternative') #Create the body of the message.
    body.attach(MIMEText(user_msg)) #Define a message type of MIMEText from user input
    msg.attach(body) #Attach the body to the message
    
    file = results # This is the file you are getting the results from.
    attachment = MIMEBase('application', "octet-stream") #Set up the foundation for the attachment
    attachment.set_payload( open(file,"rb").read() ) #Open the file and read in the contents
    Encoders.encode_base64(attachment) #Encode the message into base64
    attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) #Add the header information for just the attachment, this way you can download the attachment
    msg.attach(attachment) #add the attachment to the message
    
    msg.add_header('From', gmail_user) #Set the header fields for the message. This is the From header.
    msg.add_header('To', to) #To header
    msg.add_header('Subject', subject) #Subject header
    msg.add_header('Reply-To', gmail_user) #Reply-To header. Here it is set to the same as the From header.
    
    header = '\n\nTo:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' + subject + ' \n' #Compile header information to be printed to stout
    print header #Print the header information
    print user_msg + '\n' #Print the user provided message
    smtpserver.sendmail(gmail_user, to, msg.as_string()) # Now it is time to send the actual email.
    print '\nSent!' #You have successfully send the email
    smtpserver.close() #Close the smtp session.
    
if __name__ == "__main__":  #Main function
    
    #These are checks for user input
    files_desg=["f","F","file","File"]
    dir_desg=["d","D","dir","Dir","directory","Directory"]
    exit_cmd=["exit","Exit","e","E"]    
    stop_cmd=["s","S","stop","Stop"]
    yes_cmd=["y","Y","yes","Yes"]
    no_cmd=["n","N","no","No"]
    
    results = open("results.txt", "wr") #Open the results file so you can write to it.  You could add in a section to create it as well if needed.
    
    while 1: #Keep going while true.
        type = raw_input("Are you checking a file or a directory [f,d,exit]: ") #See if the user wants to check just one file or a directory
        if type in files_desg: #This is the option for files.
            cont = True #Boolean statement to keep the upcoming while loop going.  This way the user can check multiple files without checking an entire tree.
            while cont: #Keep going will true
                selc = raw_input("Please pass a file to be checked [stop]: ") #Input stop to break the while loop
                if selc in stop_cmd:
                    cont = False
                else: #Well they didn't stop so lets check the file
                    try: #Try to check the user provided file.
                        
                        #Group Checks
                        print("File: " + get_path(selc) + " owned by " + get_owner(selc) + " and group " + get_group(selc) + " has the following permissions: ") #Print to stdout the file information    
                        add_results(results, "File: " + get_path(selc) + " owned by " + get_owner(selc) + " and group " + get_group(selc) + " has the following permissions: \n") #Add the file information to the results file
                        if group_readable(selc): #Group Readable check
                            add_results(results, "\tFile: " + selc + " is group readable\n")
                            print("\tFile: " + selc + " is group readable")
                        if group_writeable(selc): #Group writeable check
                            add_results(results, "\tFile: " + selc + " is group writeable\n")
                            print("\tFile: " + selc + " is group writeable")
                        if group_executable(selc): #group executable check
                            add_results(results, "\tFile: " + selc + " is group executable\n")
                            print("\tFile: " + selc + " is group executable")
            
                        #World Checks
                        if world_readable(selc): #World readable check
                            add_results(results, "\tWARNING! File: " + selc + " is world readable\n")
                            print("\tWARNING! File: " + selc + " is world readable")
                        if world_writeable(selc): #World writeable check
                            add_results(results, "\tWARNING! File: " + selc + " is world writeable\n")
                            print("\tWARNING! File: " + selc + " is world writeable")
                        if world_executable(selc):#world executable check
                            add_results(results, "\tWARNING! File: " + selc + " is world executable\n")
                            print("\tWARNING! File: " + selc + " is world executable")

                    except OSError: #The user provided a bad location
                        print("Please enter a valid location")
        elif type in dir_desg: #The user wants to check a directory
            cont = True
            while cont:
                selc = raw_input("Please pass a directory to be checked [stop]: ") #Once again stop to break out of loop
                if selc in stop_cmd:
                    cont = False
                else:
                    try: #Make sure the directory is vaild
                        for filename in os.listdir(selc): #Check every file in the directory provided by the user
                            print("File: " + get_path(filename) + " owned by " + get_owner(filename) + " and group " + get_group(filename) + " has the following permissions: ")   #stdout info for the file being checked 
                            add_results(results, "File: " + get_path(filename) + " owned by " + get_owner(filename) + " and group " + get_group(filename) + " has the following permissions: \n") #file info printed to the results file
                            #Group Checks
                            if group_readable(filename): #Group Readable?
                                add_results(results,"\tFile: " + filename + " is group readable.\n")
                                print("\tFile: " + filename + " is group readable.")
                            if group_writeable(filename): #Group Writeable?
                                add_results(results,"\tFile: " + filename + " is group writeable.\n")
                                print("\tFile: " + filename + " is group writeable.")
                            if group_executable(filename): #Group Executable?
                                add_results(results,"\tFile: " + filename + " is group executable.\n")
                                print("\tFile: " + filename + " is group executable.")
            
                            #World Checks
                            if world_readable(filename): #World readable?
                                add_results(results,"\tWARNING! File: " + filename + " is world readable.\n")
                                print("\tWARNING! File: " + filename + " is world readable.")
                            if world_writeable(filename): #World writeable
                                add_results(results,"\tWARNING! File: " + filename + " is world writeable.\n")
                                print("\tWARNING! File: " + filename + " is world writeable.")
                            if world_executable(filename):#World executable
                                add_results(results,"\tWARNING! File: " + filename + " is world executable.\n")
                                print("\tWARNING! File: " + filename + " is world executable.")
                    except OSError: #They provided a bad location
                        print("Please enter a valid location")
        elif type in exit_cmd: #The user is ready to exit the program
            results.close() #Close the results file. We are done writing to it.
            selc = raw_input("Thank You for using the permissions checking script. Would you like to email yourself the results [y,n]: ") #Check to see if the user wants an email with results
            if selc in yes_cmd: #They want an email
                try: #See if you can email the user.
                    email_me(results) #Attempt to email
                    print("You have been emailed the results. Have a good day!")
                #finally: #Use finally true if you are having errors and need to see the SMTP exception that is being thrown.
                    #True
                except smtplib.SMTPException: #Catch any errors
                    print("Unable to email you the results.  Sorry about that!")
            else: # Well you didn't want a email huh
                print("Have a good day!")
            sys.exit(0) #Close the program
        else: #You didn't pick directory or file or exit.  Try again and pick a valid option.
            print("Please choose a valid selection") 
    
