import sys, os, shutil, platform, requests, zipfile

# FOR TESTING
# REMOVES SERVER FOLDER EVERY RUN
# might leave it in to help eliminate errors... (please don't)
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
    # ask if jdk needs to be installed and install if needed
    instJDK = input("Install OpenJDK 17? (Y/N): ")
    if instJDK != "": instJDK == instJDK.lower()[0]
    if instJDK == "n": print("skipping jdk installation...")
    else:
        #--- donwload zip
        print("downloading OpenJDK 17... (this can take a few minutes)")
        response = requests.get(
            'https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip',
        ) 
        with open('openjdk17.zip', 'wb') as f:
            f.write(response.content)
        #--- unpack zip
        print("unpacking OpenJDK 17...")
        with zipfile.ZipFile("openjdk17.zip", "r") as zip:
            zip.extractall("./servers/")
        #--- cleanup zip
        print("cleaning up files...")
        os.remove("openjdk17.zip")
    
    print("downloading minecraft setup.py file...")
    #todo
        
    
def setupMCLin(folder):
    #get dependencies installed
    print("installing dependencies...")
    os.system("sudo apt update && sudo apt upgrade && sudo apt install openjdk-17-jre-headless")

    #create setup file by curl
    print("downloading minecraft setup.py file...")
    #todo
    
def displayHelp():
    print("python setup.py -m(inecraft)|-s(team)|-b(oth)")
    
def makeFolder(path):
    if not os.path.exists(path): os.makedirs(path)
    
main(sys.argv)