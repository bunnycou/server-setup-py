import sys, os, shutil, platform, requests, zipfile
from random import randint

# FOR TESTING
# REMOVES SERVER FOLDER EVERY RUN
if os.path.exists("servers"): shutil.rmtree("servers")

def main(args):
    osType = platform.system()
    setupMC(osType)
        
def setupMC(osType):
    #make folders
    folder = "./servers/"
    makeFolder(folder)
    
    #create files based on os version
    if osType == "Windows": setupMCWin(folder)
    elif osType == "Linux": setupMCLin(folder)
    elif osType == "Darwin": print("MacOS is not Supported")

def setupMCWin(folder):
    print("Setting up for Windows")
    
    #--- download zip
    print("downloading OpenJDK 17... (this can take a few minutes)")
    response = requests.get(
        "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip",
    ) 
    with open("openjdk17.zip", "wb") as f:
        f.write(response.content)
    #--- unpack zip
    print("unpacking OpenJDK 17...")
    with zipfile.ZipFile("openjdk17.zip", "r") as zip:
        zip.extractall("./servers/")
    os.rename("./servers/jdk-17.0.2/", "./servers/jdk/")
    #--- cleanup zip
    print("cleaning up files...")
    os.remove("openjdk17.zip")
    
    #--- download mcsetupwin.py
    print("downloading minecraft setup.py file...")
    response = requests.get(
        f"https://raw.githubusercontent.com/bunnycou/server-setup-py/main/mcsetupWIN.py?{randint(0,999)}", # rand int is to make sure curl grabs the most recent version
    ) 
    with open(f"{folder}\\setup.py", "wb") as f:
        f.write(response.content)
    
def setupMCLin(folder):
    print("Setting up for Linux...")
    
    #get dependencies installed
    print("installing dependencies...")
    os.system("sudo apt update && sudo apt upgrade && sudo apt install openjdk-17-jre-headless")

    #create setup file by curl
    print("downloading minecraft setup.py file...")
    response = requests.get(
        f"https://raw.githubusercontent.com/bunnycou/server-setup-py/main/mcsetupLIN.py?{randint(0,999)}",
    ) 
    with open(f"{folder}/setup.py", "wb") as f:
        f.write(response.content)
    
def displayHelp():
    print("python setup.py -m(inecraft)|-s(team)|-b(oth)")
    
def makeFolder(path):
    if not os.path.exists(path): os.makedirs(path)
    
main(sys.argv)