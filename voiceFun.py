import wave
import sounddevice as sd
import numpy as np
from threading import Event
import os
import glob
import json


 
 


class SdRecord():
    def __init__(self):
        f = open("setting.json")
        data = json.load(f)
        sd.default.device="Stereo Mix (Realtek High Definition Audio), Windows DirectSound"
        self.SAMPLE_RATE = data["audio"]["SAMPLE_RATE"]  
        self.CHANNELS = data["audio"]["CHANNELS"]  
        self.DURATION =  data["audio"]["DURATION"]  
        self.audio_data = []
        self.isRecord=Event()
        self.WAVE_OUTPUT_FILENAME =data["audio"]["WAVE_OUTPUT_FILENAME"]
        self.WAVE_OUTPUT_FOLDER=data["audio"]["WAVE_OUTPUT_FOLDER"]

        s = sd.query_devices()
        print(s)

    def record(self):

        print ("recording...")
        self.audio_data=[]
        with sd.InputStream(samplerate=self.SAMPLE_RATE, channels=self.CHANNELS, dtype='int16', callback=self.callback):
            while not self.isRecord.is_set():

                sd.sleep(10) 
    def callback(self,indata,time, frames, status):
        """ This function is called for each audio block """

        self.audio_data.append(indata.copy())  
    def stop(self):
        self.isRecord.set()
        print("saving...")
        self.delF()
        self.audio_data = np.concatenate(self.audio_data, axis=0) 
        with wave.open(self.WAVE_OUTPUT_FOLDER+self.WAVE_OUTPUT_FILENAME+".wav", "wb") as wf:

            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)  
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(self.audio_data.tobytes())
        print("saved")
        self.isRecord.clear()

    
    def delF(self):
        files = glob.glob(self.WAVE_OUTPUT_FOLDER+"*")
        for f in files:
             os.remove(f)
