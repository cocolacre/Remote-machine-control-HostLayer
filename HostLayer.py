#author: Smirnov Vadim @ cocolacre
import threading
import time,os,sys,time,random,math,datetime,email,imaplib,base64,itertools,ctypes,logging
import subprocess as sp
import tkinter
import collections
import sqlite3
import socket
import codecs
from pathlib import Path
from tkinter import *
from tkinter import filedialog
import random as rn
ri = rn.randint
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.server
import xmlrpc.client



#class CustomXMLRPCServer(SimpleXMLRPCServer):
    
#    pass

class CustomRequestHandler(SimpleXMLRPCRequestHandler):
    #def __init__(self, *args, **kwargs):
    def __init__(self, request,client_address,server):
        self.allowed_IPs = ["109.252.68.252"]#my ip
        #print(self.client_address)
        #if self.client_address[0] in self.allowed_IPs:
        if client_address[0] in self.allowed_IPs:
            print(client_address[0] +" ok you're in.")
            #super().__init__(*args, **kwargs)
            SimpleXMLRPCRequestHandler.__init__(self,request,client_address,server)
            
        else:
            print("WARNING! Alien IP attempted to execute XMLRPC: " + client_address[0])
            
        
        
class HostLayer():
    def __init__(self):
        self.pid = os.getpid()
        self.default_params = {}
        self.params = {} #stores all program parameters.
        self.read_or_create_config()
        self.init_fine_control_ui()
        self.health_check_work_files()
        self.ip = "?.?.?.?"
        self.ip = self.get_host_ip()
        self.port_heartbeat = 228
        self.port = 228
        self.server = SimpleXMLRPCServer((self.ip, self.port),requestHandler= CustomRequestHandler,allow_none=True)
        self.attr_x = "x"
        self.register_functions()
        os.system("mkdir Scripts")
        os.system("mkdir Logs")
    def __info__(self):
        print("This module runs on host OS, accepts tasks from FrontLayer, runs processes on virtual machines and collects results")
    def get_uptime(self):
        MODE = 1
        if MODE == 0:
            res = sp.check_output("systeminfo")
            z,w = "",""
            for x in res.decode("utf-16").split("\r\n"):
                print(x[:20],"Время" in x)
                
                if "System Boot" in x or "Время загрузки" in x:
                    for y in x.split(" "):
                        if y.count("2020") == 1:
                            z = y.strip().replace(",","")
                            #print(z)
                        if y.count(":") == 2:
                            w = y.strip()
                            #print(w)
                    time_started = z + " " + w
                    print("[" + time_started + "]")
                    #[8/6/2020 13:28:06]
            t = time.mktime(time.strptime(time_started,"%m/%d/%Y %H:%M:%S"))
            t0 = time.time()
            t_delta = int(t0 - t)
            _h = t_delta // 3600
            _m  = (t_delta % 3600) % 60
            uptime_hours = str(_h)
            #print(uptime)
            return uptime_hours
        else:
            res = sp.check_output("wmic os get lastbootuptime",shell=True)
            res = res.decode("utf-8")
            #print("res: ", res)
            lines_res = res.split("\r\n")
            for line_res in lines_res:
                if "2020" in line_res:
                    _t=line_res.split(".")[0].strip()
                    _t = _t.replace("\r","")
                    _t = _t.replace("\n","")
                    _t = _t.replace(" ","")
                    Y = res[:4]
                    M = res[4:6]
                    D = res[6:8]
                    H = res[8:10]
                    m =res[10:12]
                    t = time.mktime(time.strptime(_t,"%Y%m%d%H%M%S"))
                    t0 = time.time()
                    t_delta = int(t0-t)
                    _h = t_delta // 3600
                    uptime_hours = str(_h)
                    return uptime_hours
            return "???"    
    def get_host_ip(self):
        with open("C:\\FOLDER\\FOLDER2\\server_ip.txt","r") as fsip:
            for line in fsip:
                if line.count(".") == 3:
                    IP = line.strip()
                    self.ip = IP
                    break
        return self.ip

    def read_or_create_config(self):
        #config is hardcoded to be in C:\FOLDER\FOLDER2\xmlrpc
        #if Path("C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini").exists():
        #    config_data = open("C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini","rb").read().decode("utf-8")
        if not Path("C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini").exists():
            with open("C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini","w+") as fconf_init:
                self.default_params["version"]="0.0.0.?"
                self.default_params["VMWARE invenrory file"]="C:\\Users\\Admin\\AppData\\Roaming\VMWare\\intentory.vmls"
                self.default_params["Config absolute path"]="C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini"
                self.default_params["VMWare binary folder"]="C:\\Program Files (x86)\\VMware\\VMware Workstation"
                self.default_params["vmrun path"]="C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"
                for item in self.default_params:
                    fconf_init.write(item + "====" + self.default_params[item] + "\n")
                    
                    
                #self.default_params["version"]="0.0.0.?"
                #self.default_params["version"]="0.0.0.?"
                #self.default_params["version"]="0.0.0.?"
        with open("C:\\FOLDER\\FOLDER2\\xmlrpc\\HostLayerConfig.ini","r") as fconf:
            for line in fconf:
                try:
                    _k  = line.split("====")[0]
                    _v = line.split("====")[1].strip()
                    self.params[_k] = _v
                    
                except Exception as _e:
                    pass
    def server_receive_file(self, arg, filename,script=True):
        
        #print(server.requestHandler.address_string())
        curDir = os.path.dirname(os.path.realpath(__file__))
        if script == True:
            output_file_path = curDir + '/Scripts/' + filename
        else:
            output_file_path = curDir + '/' + filename
        print('output_file_path -> ({})'.format(output_file_path))
        with open(output_file_path, "wb") as handle:
            handle.write(arg.data)
            print('Output file: {}'.format(output_file_path))
            return "File saved to host: " + filename
    def run_subprocess_thread(self,command):
        
        def run_thread(command):
            res = sp.Popen(command,shell=True)
        _thread = threading.Thread(target = run_thread,args=(command,))
        _thread.start()
    
    def init_fine_control_ui(self):
        #via ctypes\tkinter\WebView\browser-access.
        #self.servers_off_button = 
        pass
    def check_or_init_heartbeat_service(self):
        pass
    def health_check_work_files(self):
        # check vm-run,vmx files,fil and other magic folders
        # logfile, config, expected value, ping, hook uptime,
        # load parameters,check duplicate processes, check message of previous instance, ggg server machines photonic gates,
        pass
    def how_many_vms_working(self):
        res = sp.check_output("vmrun.exe list")
        
        pass
    
    def stop_all_servers(self):
        pass
    def start_all_servers(self):
        pass
    def start_starred_servers(self,delay_between = 30):
        username = os.environ['USERNAME']
        inventory = "C:\\Users\\" + username + "\\AppData\\Roaming\\VMWare\\inventory.vmls"
        def start_vm(vm):
            """
            vm Example:
                "C:\VM\1.vmx"
                (should include double quotes)
            """
            def start_subproc(vm):
                cmd = '"C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe" -T ws start %s'%vm
                #subproc = sp.check_output(cmd,shell=True)
                subproc = sp.Popen(cmd,shell=True)
            x = threading.Thread(target = start_subproc,args=(vm,))
            x.start()

        with codecs.open(inventory,"r", "utf-8") as f:
            last_vm = ""
            isStarred = False
            for line in f:
                if line.find(".config = ") != -1:
                    print("...")
                    last_vm = line[len(".config = ")+line.find(".config = "):].strip()
                    #cmd = '"C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe" -T ws stop %s'%last_vm
                if line.find("sFavorite") != -1:
                    if line.find("TRUE") != -1:
                        isStarred = True
                        try:
                            print("Starting: ["+last_vm+"]")
                            start_vm(last_vm)
                            time.sleep(delay_between)
                        except Exception as _e:
                            print(str(_e))
                    else:
                        isStarred = False
    
    def stop_starred_servers(self):
        username = os.environ['USERNAME']
        inventory = "C:\\Users\\" + username + "\\AppData\\Roaming\\VMWare\\inventory.vmls"
        def stop_vm(vm):
            """
            vm Example:
                "C:\VM\1.vmx"
                (should include double quotes)
            """
            def stop_subproc(vm):
                cmd = '"C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe" -T ws stop %s'%vm
                #subproc = sp.check_output(cmd,shell=True)
                subproc = sp.Popen(cmd,shell=True)
            x = threading.Thread(target = stop_subproc,args=(vm,))
            x.start()

        with codecs.open(inventory,"r", "utf-8") as f:
            last_vm = ""
            isStarred = False
            for line in f:
                if line.find(".config = ") != -1:
                    print("...")
                    last_vm = line[len(".config = ")+line.find(".config = "):].strip()
                    #cmd = '"C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe" -T ws stop %s'%last_vm
                if line.find("sFavorite") != -1:
                    if line.find("TRUE") != -1:
                        isStarred = True
                        try:
                            print("Stopping: ["+last_vm+"]")
                            stop_vm(last_vm)
                            time.sleep(1)
                        except Exception as _e:
                            print(str(_e))
                    else:
                        isStarred = False

    def start_and_disable_checker(self):
        pass
    
    def server_execute_subprocess(self):
        pass
    def restart_xmlrpc_server(self):
        pass
    def send_to_client(self,fname):
        print("Sending %s to client"%fname)
        try:
            fhandle = open(fname,"rb")
            binary_data = xmlrpc.client.Binary(fhandle.read())
            fhandle.close()
            return data
        except Exception as _e:
            print(str(_e))
            return False
            
    def register_functions(self):
        self.server.register_function(self.server_execute_subprocess, 'server_execute_subprocess')
        self.server.register_function(self.server_receive_file, 'server_receive_file')
        #self.server.register_function(self.list_files_fil, 'list_files_fil')
        self.server.register_function(self.restart_xmlrpc_server, 'restart_xmlrpc_server')
        self.server.register_function(self.get_host_ip,"get_host_ip")
        self.server.register_function(self.get_uptime,"get_uptime")
        self.server.register_function(self.start_starred_servers,"start_starred_servers")
        self.server.register_function(self.stop_starred_servers,"stop_starred_servers")
        self.server.register_function(self.run_subprocess_thread,"run_subprocess_thread")
        self.server.register_function(self.send_to_client,"send_to_client")
        #self.server.register_function(self.read_process_memory,"read_process_memory")
    
if __name__ == "__main__":
    LOAD_GUI = True
    LOAD_GUI = False
    hl = HostLayer()
    hl.server.serve_forever()
    print("serving forever")
    if LOAD_GUI:
        gui = Tk()
        gui.configure(background="White")
        gui.title("Host Layer automation")
        #top = Tkinter.Tk()
        #top.mainloop()
        #
        b1 = Button(gui,text="Stop all servers", command = hl.stop_all_servers())
        b2 = Button(gui,text="Start all servers",command = hl.start_all_servers())
        b1.grid(row=0,column=0)
        b2.grid(row=1,column=0)
        b3 = Button(gui,text="Toogle auto ban replacement",command = lambda x: print("TOOGLE!"), height=1,width=22)
        b3.grid(row=2,column=0)
        b4 = Button(gui,text = "Update actual info for all VMs",command = lambda x: print("Updating info..."), height=1,width=22)
        b4.grid(row=3,column=0)
        b5 = Button(gui,text = "Run script for selected VMs",command = lambda x : print("RUNNING SCRIPTS"), height = 1,width=22)
        b5.grid(row=4,column=0)
        #global b6
        global fn_string_var
        fn_string_var = StringVar()
        def getText():
            fn = filedialog.askopenfilename()
            #fscript = open(fn)
            #s = fscript.read()
            fn_string_var.set(fn.split("/")[-1:])
            return fn
            
        b6 = Button(gui,text="Select script",command = getText)
        b6.grid(row=5,column=0)
        fn_string_var.set("...")
        l1 = Label(gui,textvariable= fn_string_var)
        l1.grid(row=6,column=0)
        
        #def check_vt(vt):
        #    pass
        global checked
        checked = {}
        
        def toogle_checked():
            vt  = "1"
            checked[vt] = not checked[vt]
        vars_int = {}    
        for i in range(1,26):
            vars_int[i] = BooleanVar()
            
            checked[i]=False
            table_entry = Entry(gui,width=8,bg="Grey",font=("Arial",16,"bold"))
            table_entry.grid(row=i-1,column=3)
            table_entry.insert(END,str(i)+"vt")
            vt_checkbutton = Checkbutton(gui,text="",variable=vars_int[i],command = toogle_checked)
            vt_checkbutton.grid(row=i-1,column=2)
        gui.mainloop()
    
    
