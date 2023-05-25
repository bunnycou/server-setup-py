import sys, os, requests, shutil

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
    print("Paper not implemented")
    
def setupPurpur(ver, name):
    print("downloading purpur...")
    response = requests.get(
        f"https://api.purpurmc.org/v2/purpur/{ver}/latest/download",
    ) 
    with open(f"{name}/purpur-{ver}.jar", "wb") as f:
        f.write(response.content)
    print("creating base files...")
    makeFiles(name, ver, "purpur")
    #make both executable
    os.system(f"cd ./{name} && chmod +x start && chmod +x tmuxstart")
    print("running once to generate files...")
    os.system(f"cd ./{name} && java -jar purpur-{ver}.jar")
    print("Make sure to accept the eula!")

def setupFabric(ver, name):
    print("Fabric not implemented")
    
    
def makeFolder(path):
    if not os.path.exists(path): os.makedirs(path)
    else: shutil.rmtree(path), os.makedirs(path)
        
def makeFiles(path, ver, type):
    with open(f"{path}/start", "+w") as f:
        f.write(
f"""while true
do
java -Xmx4G -jar {type}-{ver}.jar
echo server crashed! restarting in 5 seconds...
sleep 5s
done"""
            ) # requires delay otherwise it will permanently restart
        
    with open(f"{path}/tmuxstart", "+w") as f:
        f.write(f"tmux new -d -s{path} ./start")

main(sys.argv)