# coding: utf-8
import os
import zipfile
import time
import threading
import tkinter as tk
import shutil

class MCbackup():
    x = False
    running = False
    wait_time = 0
    remain_time = 0
    tx = True
    start_t=time.time()

    def zip_dir(self,path):
        zf = zipfile.ZipFile(('{}.zip').format(path), 'w', zipfile.ZIP_DEFLATED)
       
        for root, dirs, files in os.walk(path):
            for file_name in files:
                rname = root[len(self.to):]
                print("copy "+os.path.join(rname, file_name))
                zf.write(os.path.join(root, file_name),arcname=os.path.join(rname, file_name))
        zf.close()
        
    def backup(self):
        f= open('./config.txt',"r")
        tp_in = f.readline()
        tpo=tp_in.split()
        tpo.pop(0)
        worldname=tpo[0]
        tpo.pop(0)
        for i in tpo:
            worldname += (" "+i)
        tp_in = f.readline()
        self.wait_time = int(tp_in.split()[1])
        f.close()
        self.des = "C:/Users\jerem/AppData/Roaming/.minecraft/saves"
        self.to = "C:/Users\jerem/AppData/Roaming/.minecraft/backup"
        path = self.to+"/"+worldname
        if not os.path.exists(self.des+"/"+worldname):
            self.T.insert(tk.END,"folder '"+worldname+"' not exsit.\n")
            self.B['text']="start"
            self.T.insert(tk.END, "stop\n")
            self.x=False
            return 0
        try:
            os.mkdir(self.to)
        except OSError:
            print ("Creation of the directory '/backup' failed")
        else:
            print ("Successfully created the directory 'backup' ")  
        
        self.start_t=time.time()
        tptime=time.localtime()
        try:
            add="-"+str(tptime.tm_year)+"-"+str(tptime.tm_mon)+"-"+str(tptime.tm_mday)+"--"+str(tptime.tm_hour)+"-"+str(tptime.tm_min)
            self.T.insert(tk.END, "Start backup...\n")
            self.running = True
            shutil.copytree(self.des+"/"+worldname, self.to+"/"+worldname+add, ignore=shutil.ignore_patterns('session.lock'))
            self.zip_dir(path+add)
            shutil.rmtree(self.to+"/"+worldname+add)
            print("create file "+worldname+add+".zip successfully")
            self.T.insert(tk.END, "create file "+worldname+add+".zip successfully\n")
        except:
            print("some error occur when creating zip file")
            self.T.insert(tk.END,"some error occur when creating zip file\n")
        self.running = False
        while self.x:
            time.sleep(1)
            if time.time()-self.start_t >= self.wait_time*60:
                self.start_t=time.time()
                tptime=time.localtime()
                try:
                    add="-"+str(tptime.tm_year)+"-"+str(tptime.tm_mon)+"-"+str(tptime.tm_mday)+"--"+str(tptime.tm_hour)+"-"+str(tptime.tm_min)
                    self.T.insert(tk.END, "Start backup...\n")
                    self.running = True
                    shutil.copytree(self.des+"/"+worldname, self.to+"/"+worldname+add, ignore=shutil.ignore_patterns('session.lock'))
                    self.zip_dir(path+add)
                    shutil.rmtree(self.to+"/"+worldname+add)
                    print("create file "+worldname+add+".zip successfully")
                    self.T.insert(tk.END, "create file "+worldname+add+".zip successfully\n")
                except:
                    print("some error occur when creating zip file")
                    self.T.insert(tk.END,"some error occur when creating zip file\n")
                self.running = False
        self.start_t = 0
                
    def Timer(self):
        while self.tx:
            self.remain_time = self.wait_time*60-time.time()+self.start_t
            if self.remain_time > 0:
                self.time_label_1['text']='Remain Time: '+ str(int(self.remain_time/60)) +":"+str(int(self.remain_time%60))
            else:
                self.time_label_1['text']='Remain Time: 00:00'
            time.sleep(1)


    def __init__(self):

        self.time_thread = threading.Thread(target = self.Timer)

        
        self.window = tk.Tk()
        # 設定視窗標題、大小和背景顏色
        self.window.title('MCbackup')
        self.window.geometry('400x300')
        self.window.configure(background='gray')
        
        header_label = tk.Label(self.window, text='MC Backup', font=20, height= 0)
        header_label.pack()


        self.B = tk.Button(self.window, text = "start", command = self.start,bg="yellow")
        self.B.pack()

        self.time_label_1 = tk.Label(self.window, text=' ', font=12, height= 0)
        self.time_label_1.pack()

        self.time_thread.start()
        
        self.S = tk.Scrollbar(self.window)
        self.T = tk.Text(self.window)
        self.S.pack(side=tk.RIGHT,fill=tk.BOTH)
        self.T.pack(side=tk.LEFT,fill=tk.BOTH)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        #self.T.insert(tk.END, "hihi")

                
        self.window.mainloop()
        self.x=False
        self.tx = False
        try:
            self.test_thread.join()
            self.time_thread.join()
            print("thread closed")
        except:
            print("bye!")
    def start(self):
        if self.running:
            self.T.insert(tk.END, "Doing backup. Please try again later.\n")
            return 0
        if not self.x:
            self.B['text']="stop"
            self.T.insert(tk.END, "start\n")
            self.x=True
            self.test_thread = threading.Thread(target = self.backup)
            self.test_thread.start()
        else:
            self.B['text']="start"
            self.T.insert(tk.END, "stop\n")
            self.x=False
            self.test_thread.join()
            print("thread closed")
    #def close(self):
        

app = MCbackup()
