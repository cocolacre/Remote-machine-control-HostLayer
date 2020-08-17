def update_HostLayer(self,new_version_file="updates\\HostLayer.py"):
    #if update check yields version other then the current one, call this...
    #need to cast update.bat\rollback.bat
    so.Popen("mkdir updates")
    so.Popen("mkdir updates\\%s"%self.version)
    sp.Popen("move HostLayer.py updates\\{0}\\HostLayer.py".format(self.version))
    self.set_config("Previous version", self.version)
    sp.Popen("update.bat")
    #add logging
    print("add logging")
def initiate_version_rollback(self):
    #on bad update and programm exception.
    sp.Popen("rollback.bat")
def set_config(self,key,value):
    # boilerplate for HostLayer class.
    kv={}
    with open(self.config_file,"r") as fc:
        for line in fc:
            k=line.split("====")[0]
            v=line.split("====")[1].strip()
            kv[k]=v
    kv[key]=value
    with open(self.config_file,"w") as fc:
        for item in kv:
            fc.write(kv +"===="+kv[item]+"\n")
            self.config[kv]=item
    