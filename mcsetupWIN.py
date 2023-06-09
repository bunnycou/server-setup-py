import sys, os, requests, shutil, json

# python setup.py -pa(per)|-pu(rpur)|-f(abric) -v [version number] -n [name]
def main(args):
    sampleText = "python setup.py -pa(per)|-pu(rpur)|-f(abric) -v [version number] -n [name-NO-SPACES]"
    if len(args) != 6: 
        print("Proper usage is...\n"+sampleText)
    else:
        try:
            for arg in args:
                if arg.startswith("-pa"): srvType = "pa"
                if arg.startswith("-pu"): srvType = "pu"
                if arg.startswith("-f"):  srvType = "f"
            ver = args[args.index("-v")+1]
            name = args[args.index("-n")+1]
        except:
            print("One or more arguments were missing\n"+sampleText)
        
        makeFolder(name)
        
        if srvType == "pa": setupPaper(ver, name)
        if srvType == "pu": setupPurpur(ver, name)
        if srvType == "f" : setupFabric(ver, name)
        
def setupPaper(ver, name):
    print("downloading paper...")
    response = requests.get(
        f"https://api.papermc.io/v2/projects/paper/versions/{ver}/builds",
    ) 
    js = json.loads(response.content)
    build = js["builds"][-1]["build"]
        
    response2 = requests.get(
        f"https://api.papermc.io/v2/projects/paper/versions/{ver}/builds/{build}/downloads/paper-{ver}-{build}.jar",
    ) 
    with open(f"{name}\\paper-{ver}.jar", "wb") as f:
        f.write(response2.content)    
    
    print("creating base files...")
    makeFiles(name, ver, "paper")
    print("running once to generate files...")
    os.system(f"cd .\\{name} && ..\\jdk\\bin\\java -jar paper-{ver}.jar --nogui")
    print("Make sure to accept the eula!")
    
def setupPurpur(ver, name):
    print("downloading purpur...")
    response = requests.get(
        f"https://api.purpurmc.org/v2/purpur/{ver}/latest/download",
    ) 
    with open(f"{name}\\purpur-{ver}.jar", "wb") as f:
        f.write(response.content)
    print("creating base files...")
    makeFiles(name, ver, "purpur")
    print("running once to generate files...")
    os.system(f"cd .\\{name} && ..\\jdk\\bin\\java -jar purpur-{ver}.jar --nogui")
    print("Make sure to accept the eula!")

def setupFabric(ver, name):
    loadver = input("Input fabric loader version (such as 0.14.19): ")
    print("downloading fabric...")
    response = requests.get(
        f"https://meta.fabricmc.net/v2/versions/loader/{ver}/{loadver}/0.11.2/server/jar", # will have to be updated manually occasionally unfortunately...
    ) 
    with open(f"{name}\\fabric-{ver}.jar", "wb") as f:
        f.write(response.content)
    print("creating base files...")
    makeFiles(name, ver, "fabric")
    print("running once to generate files...")
    os.system(f"cd .\\{name} && ..\\jdk\\bin\\java -jar fabric-{ver}.jar --nogui")
    print("Make sure to accept the eula!\nDon't forget to add your mods and the fabric API mod in the mods folder")
    
    
def makeFolder(path):
    if not os.path.exists(path): os.makedirs(path)
    else: shutil.rmtree(path), os.makedirs(path)
        
def makeFiles(path, ver, type):
    with open(f"{path}\\start.bat", "+w") as f:
        f.write(
f"""@echo off
title {path}-{ver}
:start\n",
..\\jdk\\bin\\java -Xmx4G -jar {type}-{ver}.jar --nogui
echo server crashed! restarting...
goto start"""
            )

main(sys.argv)