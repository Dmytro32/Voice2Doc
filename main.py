import tkinter as tk
from tkinter import messagebox
import voiceFun
import model
import threading 
import doc
from time import sleep
class GUI:
    def __init__(self):
        self.recording_thread =None
        self.audio=voiceFun.SdRecord()
        root=tk.Tk()
        frame=tk.Frame(root)
        root.geometry("640x640")
           
        recButton=tk.Button(frame,text="Record",command=self.record)
        stopButton=tk.Button(frame,text="Stop",command=self.stop)
        readButton=tk.Button(frame,text="Convert audio",command=self.read)
        clearButton=tk.Button(frame,text="Clear text",command=self.clear)
        saveButton=tk.Button(frame,text="Save",command=self.save)

        self.textBox=tk.Text(root,height=200,width=200)
        mainTitle=tk.Label(root,text="Speak recogtion in ukraine")
        hintTitle=tk.Label(root,text=" For start/stop record press buttom. Edit text can be only if no recording.To save press buttom and choose doc file ")
        
        mainTitle.pack()
        hintTitle.pack()
        frame.pack( )

        recButton.pack(side=tk.LEFT)
        stopButton.pack(side=tk.LEFT)
        readButton.pack(side=tk.LEFT)
        clearButton.pack(side=tk.LEFT)
        saveButton.pack(side=tk.LEFT)
        self.textBox.pack()
        tk.mainloop()

    def record(self):
        if self.recording_thread is None or not self.recording_thread.is_alive():
            check=messagebox.askyesno(title="Monitoring",message="Start monitoring channgel")
            if check:
                self.recording_thread = threading.Thread(target=self.audio.record,daemon=True)
                self.recording_thread.start()
        else:
            messagebox.showinfo("Monitoring stop")
            print("Recording thread is already running")
    def stop(self):
        if  self.recording_thread.is_alive():
            sleep(2)
            self.audio.stop()
    def read(self):
        pred=model.openWhisper()
        print(pred)
        self.textBox.insert(tk.INSERT,pred)
    def clear(self):
        self.textBox.delete("1.0",tk.END)
    def save(self):
        text=self.textBox.get("1.0",tk.END)
        doc.save(text)
            
GUI()



