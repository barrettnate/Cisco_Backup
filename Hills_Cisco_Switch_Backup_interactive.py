# Backup Cisco config
# Nate Barrett
# Hill's Pet Nutrition
# 08/11/2023
 
#Import modules needed and set up ssh connection parameters
import paramiko
import datetime
import getpass
import os
import time



#Define variables
time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
switchLocation = input('Which site are these switches located? (ex. USEP)')
switchLocation = switchLocation.upper()
searchTerm = 'hostname'
port = 22
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Text formatting definitions
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

#These two file paths need to be changed to match the appropriate locations
#Infilepath needs to point to the text file that contains the IP addresses of the switches. 1 per line.
infilepath = "O:\\My Drive\\Powershell\\Scripts\\Switches\\{}".format(switchLocation) + "_Switches.txt"
outfilepath = "O:\\My Drive\\Powershell\\Scripts\\Switches\\Backup\\{}\\".format(switchLocation)



def createDirectory():
    #Create Directory if it doesn't exist
    isExist = os.path.exists(outfilepath)
    if not isExist:

        # Create a new directory
        os.makedirs(outfilepath)
        print("The directory wasn't found. Creating now.")

#Functions for components of the script
def switchConnect():
    
    userName = input('Username: ')
    userPass = getpass.getpass()
  
    # open device file
    input_file = open( infilepath, "r")
    iplist = input_file.readlines()
    input_file.close()
    

    for ip in iplist:
        ipaddr = ip.strip()
        ssh.connect(hostname=ipaddr, username=userName, password=userPass, port=port)
        _stdin, _stdout, _stderr = ssh.exec_command('show run')
        list = _stdout.readlines()
        searchList = [list.index(i) for i in list if searchTerm in i]
        
        #split list at line containing "hostname" to get hostname.
        indexValue = searchList[0]
        splitList = list[indexValue]
        
        #declare variables for file paths
        switchHostname = splitList.rsplit(' ',1)[-1].rstrip()
        switchOutfile = outfilepath + switchHostname + "_" + ipaddr
        combOutfile = switchOutfile + "\\"
                
        #Check if backup directory already exists
        isExist = os.path.exists(switchOutfile)
        if not isExist:

            # Create a new backup directory if it does not exist
            os.makedirs(switchOutfile)
            prLightPurple("The switch directory wasn't found. Creating it now.")

        
        #CODE TO DELETE OLD FILES BETWEEN *
        #*******************
        #declare variables
        folder = switchOutfile
        #Change this value if you want to retain files longer
        numberofDays = 7
        day = 86400
        # get the current time
        current_time = time.time()
  
        # changing the current working directory
        # to the folder specified
        os.chdir(os.path.join(os.getcwd(), folder))
  
        # get a list of files present in the given folder
        list_of_files = os.listdir()    
  
        # loop over all the files
        for i in list_of_files:
            # get the location of the file
            file_location = os.path.join(os.getcwd(), i)
            # file_time is the time when the file is modified
            file_time = os.stat(file_location).st_mtime
  
            # if a file is modified before N days then delete it
            if(file_time < current_time - day*numberofDays):
                prRed(f" Delete : {i}")
                os.remove(file_location)
            else :
                print("No files older than " + str(numberofDays) + " days old were found.\n\n")
        #******************************************

        #Connect to switch and copy running config
        prGreen("Connecting to cisco switch " + switchHostname + "\n")
        outfile = open(combOutfile + switchHostname + "_" + ipaddr + "-" + time_now, "w")
        for char in list:
            outfile.write(char)
        ssh.close()
        outfile.close()


      
#Only use this function for a single folder
def deleteOldFiles():
  
    #declare variables
    folder = switchOutfile
    numberofDays = 1
    day = 86400
    # get the current time
    current_time = time.time()
  
    # changing the current working directory
    # to the folder specified
    os.chdir(os.path.join(os.getcwd(), folder))
  
    # get a list of files present in the given folder
    list_of_files = os.listdir()    
  
    # loop over all the files
    for i in list_of_files:
        # get the location of the file
        file_location = os.path.join(os.getcwd(), i)
        # file_time is the time when the file is modified
        file_time = os.stat(file_location).st_mtime
  
        # if a file is modified before N days then delete it
        if(file_time < current_time - day*numberofDays):
            prRed(f" Delete : {i}")
            os.remove(file_location)
        else :
            print("No files older than " + str(numberofDays) + " days old were found.\n\n")
    
    
    
    
    

#Main Function
def main():
    createDirectory()
    switchConnect()

#Calling main function
main()