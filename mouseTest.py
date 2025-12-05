import sounddevice as sd
import numpy as np
import pyautogui  # For mouse clicks
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import json

def record_chunk(seconds=1, samplerate=16000):
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
    sd.wait()
    return audio.squeeze()
def get_set():
    f = open("setting.json")
    set = json.load(f)
    return set
def openWhisper():
    set=get_set()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = set["model"]["model_id"]
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe

pipe= openWhisper()

while True:
    audio_chunk = record_chunk(0.75)
    result = pipe(audio_chunk)["text"].strip().lower()
    print("Heard:", result)
    
    if "click" in result:
        pyautogui.click()
        print("Mouse clicked!")
